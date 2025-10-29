"""Data update coordinator for Growatt Modbus Integration."""
import asyncio
import logging
from datetime import datetime, timedelta, time
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.event import async_track_time_change

from .const import (
    DOMAIN,
    CONF_SLAVE_ID,
    CONF_REGISTER_MAP,
    REGISTER_MAPS,
    get_sensor_type,
    SENSOR_OFFLINE_BEHAVIOR,
)
from .growatt_modbus import GrowattModbus, GrowattData

_LOGGER = logging.getLogger(__name__)

# Map old register map names to new ones for migration
REGISTER_MAP_MIGRATION = {
    'MIN_10000_VARIANT_A': 'MIN_10000_TL_X_OFFICIAL',
    'MIN_10000_CORRECTED': 'MIN_10000_TL_X_OFFICIAL',
    'MIN_SERIES_STANDARD': 'MIN_10000_TL_X_OFFICIAL',
}


def test_connection(config: dict) -> dict:
    """Test the connection to the Growatt inverter (TCP only)."""
    try:
        # Migrate old register map names
        register_map = config.get(CONF_REGISTER_MAP, 'MIN_7000_10000TL_X')
        register_map = REGISTER_MAP_MIGRATION.get(register_map, register_map)
        
        # Ensure register map exists
        if register_map not in REGISTER_MAPS:
            register_map = 'MIN_7000_10000TL_X'
        
        # Create the TCP modbus client (TCP-only)
        client = GrowattModbus(
            connection_type="tcp",
            host=config[CONF_HOST],
            port=config[CONF_PORT],
            slave_id=config[CONF_SLAVE_ID],
            register_map=register_map
        )
        
        # Test connection
        if client.connect():
            # Try to read some basic data
            data = client.read_all_data()
            client.disconnect()
            
            if data is not None:
                return {
                    "success": True,
                    "serial_number": data.serial_number,
                    "firmware_version": data.firmware_version,
                    "register_map": register_map
                }
            else:
                return {"success": False, "error": "Could not read data from inverter"}
        else:
            return {"success": False, "error": "Could not connect to inverter"}
            
    except Exception as err:
        _LOGGER.exception("Connection test failed")
        return {"success": False, "error": str(err)}


class GrowattModbusCoordinator(DataUpdateCoordinator[GrowattData]):
    """Growatt Modbus data update coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self.config = entry.data
        self.hass = hass
        self.last_successful_update = None
        self.last_update_success_time = None  # For timezone-aware timestamp sensor
        
        # Offline state management
        self._last_successful_read = None
        self._previous_day_totals = {}
        self._current_date = datetime.now().date()
        self._inverter_online = False
        
        # Cache for holding registers (writable settings)
        self.holding_register_cache = {}
        
        # Get update interval from options (default 30 seconds)
        scan_interval = entry.options.get("scan_interval", 30)
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.data[CONF_NAME]}",
            update_interval=timedelta(seconds=scan_interval),
        )
        
        # Initialize the Growatt client
        self._client = None
        self._initialize_client()
        
        # Set up midnight callback for daily total resets
        self._setup_midnight_callback()

    def _get_register_map(self) -> str:
        """Get register map with migration support."""
        register_map = self.config.get(CONF_REGISTER_MAP, 'MIN_7000_10000TL_X')
        
        # Migrate old register map names
        if register_map in REGISTER_MAP_MIGRATION:
            old_map = register_map
            register_map = REGISTER_MAP_MIGRATION[register_map]
            _LOGGER.info(
                "Migrating register map from '%s' to '%s'",
                old_map,
                register_map
            )
        
        # Validate register map exists
        if register_map not in REGISTER_MAPS:
            _LOGGER.warning(
                "Unknown register map '%s', falling back to MIN_7000_10000TL_X",
                register_map
            )
            register_map = 'MIN_7000_10000TL_X'
        
        return register_map

    def _initialize_client(self):
        """Initialize the Growatt Modbus client (TCP-only)."""
        try:
            register_map = self._get_register_map()
            
            # TCP-only connection
            self._client = GrowattModbus(
                connection_type="tcp",
                host=self.config[CONF_HOST],
                port=self.config[CONF_PORT],
                slave_id=self.config[CONF_SLAVE_ID],
                register_map=register_map
            )
                
            _LOGGER.info("Initialized Growatt client with register map: %s", register_map)
            
        except Exception as err:
            _LOGGER.error("Failed to initialize Growatt client: %s", err)
            self._client = None

    def _setup_midnight_callback(self):
        """Set up callback to run at midnight for daily total resets."""
        async_track_time_change(
            self.hass,
            self._handle_midnight_reset,
            hour=0,
            minute=0,
            second=0
        )
        _LOGGER.info("Midnight callback registered for daily total resets")

    async def _handle_midnight_reset(self, now=None):
        """Handle midnight reset of daily totals."""
        _LOGGER.info("Midnight reset triggered - storing previous day totals")
        
        if self.data is None:
            _LOGGER.debug("No data available for midnight reset")
            return
        
        # Store today's daily totals as "yesterday" before they reset
        self._previous_day_totals = {
            'energy_today': getattr(self.data, 'energy_today', 0),
            'energy_to_grid_today': getattr(self.data, 'energy_to_grid_today', 0),
            'load_energy_today': getattr(self.data, 'load_energy_today', 0),
            'energy_to_user_today': getattr(self.data, 'energy_to_user_today', 0),
        }
        
        # Update current date
        self._current_date = datetime.now().date()
        
        _LOGGER.debug("Previous day totals stored: %s", self._previous_day_totals)
        
        # If inverter is offline, zero out the daily totals now
        if not self._inverter_online and self.data is not None:
            _LOGGER.info("Inverter offline at midnight - resetting daily totals to 0")
            # Create modified data with zeroed daily totals
            self.data.energy_today = 0
            self.data.energy_to_grid_today = 0
            self.data.load_energy_today = 0
            self.data.energy_to_user_today = 0
            
            # Trigger update to notify sensors
            self.async_set_updated_data(self.data)

    @property
    def device_name(self) -> str:
        """Return the device name."""
        return self.config[CONF_NAME]

    def get_sensor_value(self, sensor_key: str, raw_value: Any) -> Any:
        """
        Get sensor value with smart offline behavior.
        
        Args:
            sensor_key: The sensor identifier
            raw_value: The raw value from the data
            
        Returns:
            The value to use, considering online/offline state
        """
        if self._inverter_online:
            # Inverter is online, use raw value
            return raw_value
        
        # Inverter is offline - apply offline behavior
        sensor_type = get_sensor_type(sensor_key)
        offline_behavior = SENSOR_OFFLINE_BEHAVIOR.get(sensor_type)
        
        if offline_behavior == 0:
            # Power sensors go to 0
            return 0
        elif offline_behavior == 'retain':
            # Daily and lifetime totals retain last value
            return raw_value
        elif offline_behavior == None:
            # Diagnostic sensors go unavailable
            return None
        elif offline_behavior == 'offline':
            # Status sensors show offline
            return 'offline'
        
        return raw_value

    @property
    def is_online(self) -> bool:
        """Return whether the inverter is currently online."""
        return self._inverter_online

    async def _async_update_data(self) -> GrowattData:
        """Fetch data from the Growatt inverter."""
        if self._client is None:
            raise UpdateFailed("Growatt client not initialized")

        try:
            # Run the blocking operations in executor
            data = await self.hass.async_add_executor_job(self._fetch_data)
            
            if data is None:
                # Inverter not responding (probably night time or powered off)
                self._inverter_online = False
                
                if self.data is not None:
                    _LOGGER.debug("Inverter offline - applying smart offline behavior")
                    
                    # Check if we crossed midnight while offline
                    current_date = datetime.now().date()
                    if current_date > self._current_date:
                        _LOGGER.info("Date changed while inverter offline - resetting daily totals")
                        # Reset daily totals to 0
                        self.data.energy_today = 0
                        self.data.energy_to_grid_today = 0
                        self.data.load_energy_today = 0
                        self.data.energy_to_user_today = 0
                        self._current_date = current_date
                    
                    # Return existing data (sensors will apply offline behavior via get_sensor_value)
                    return self.data
                else:
                    # First connection attempt failed
                    raise UpdateFailed("Failed to read data from inverter")
            
            # Inverter is responding!
            was_offline = not self._inverter_online
            self._inverter_online = True
            
            # Update successful - record timestamp (timezone-aware)
            from datetime import timezone as tz
            self.last_successful_update = datetime.now()
            self.last_update_success_time = datetime.now(tz.utc)
            self._last_successful_read = datetime.now()
            
            # Check for date transition (inverter came back online on new day)
            current_date = datetime.now().date()
            if was_offline and current_date > self._current_date:
                _LOGGER.info("Inverter back online after date change - daily totals already reset by inverter")
                self._current_date = current_date
                # Inverter's daily totals are already at new day values (small amounts from morning production)
            
            return data
            
        except Exception as err:
            _LOGGER.error("Error fetching data from Growatt inverter: %s", err)
            self._inverter_online = False
            
            # Keep last data if available
            if self.data is not None:
                _LOGGER.debug("Error fetching data, keeping last known data with offline behavior")
                return self.data
            raise UpdateFailed(f"Error communicating with inverter: {err}")

    def _fetch_data(self) -> GrowattData | None:
        """Fetch data from the inverter (runs in executor)."""
        try:
            if not self._client.connect():
                _LOGGER.error("Failed to connect to Growatt inverter")
                return None
                
            data = self._client.read_all_data()
            self._client.disconnect()
            
            return data
            
        except Exception as err:
            _LOGGER.error("Error during data fetch: %s", err)
            if self._client:
                try:
                    self._client.disconnect()
                except:
                    pass
            return None

    async def async_config_entry_first_refresh(self) -> None:
        """Perform first refresh and handle setup errors."""
        try:
            await super().async_config_entry_first_refresh()
            # Load holding registers for number/select entities
            await self.async_load_holding_registers()
        except UpdateFailed as err:
            _LOGGER.error("Initial setup failed: %s", err)
            raise

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information."""
        if self.data:
            return {
                "identifiers": {(DOMAIN, self.data.serial_number)},
                "name": self.config[CONF_NAME],
                "manufacturer": "Growatt",
                "model": "MIN Series",
                "sw_version": self.data.firmware_version,
                "serial_number": self.data.serial_number,
            }
        
        # Fallback device info if no data available yet
        return {
            "identifiers": {(DOMAIN, f"{self.config[CONF_HOST]}_{self.config[CONF_SLAVE_ID]}")},
            "name": self.config[CONF_NAME],
            "manufacturer": "Growatt",
            "model": "MIN Series",
        }
    
    async def async_read_holding_registers(self, start_address: int, count: int) -> dict:
        """Read holding registers and update cache."""
        if self._client is None:
            raise UpdateFailed("Growatt client not initialized")
        
        try:
            # Run in executor
            result = await self.hass.async_add_executor_job(
                self._read_holding_registers_sync, start_address, count
            )
            return result
        except Exception as err:
            _LOGGER.error(f"Error reading holding registers {start_address}: {err}")
            raise UpdateFailed(f"Error reading holding registers: {err}")
    
    def _read_holding_registers_sync(self, start_address: int, count: int) -> dict:
        """Synchronous read of holding registers."""
        try:
            if not self._client.connect():
                _LOGGER.error("Failed to connect to inverter for reading holding registers")
                return {}
            
            registers = self._client.read_holding_registers(start_address, count)
            self._client.disconnect()
            
            if registers is None:
                return {}
            
            # Update cache
            result = {}
            for i, value in enumerate(registers):
                address = start_address + i
                self.holding_register_cache[address] = value
                result[address] = value
            
            return result
        except Exception as err:
            _LOGGER.error(f"Error reading holding registers: {err}")
            if self._client:
                try:
                    self._client.disconnect()
                except Exception as disconnect_err:
                    _LOGGER.debug(f"Error during disconnect after read failure: {disconnect_err}")
            return {}
    
    async def async_write_holding_register(self, address: int, value: int) -> None:
        """Write a single holding register."""
        if self._client is None:
            raise UpdateFailed("Growatt client not initialized")
        
        try:
            # Run in executor
            success = await self.hass.async_add_executor_job(
                self._write_holding_register_sync, address, value
            )
            
            if not success:
                raise UpdateFailed(f"Failed to write to register {address}")
            
            # Update cache
            self.holding_register_cache[address] = value
            
        except Exception as err:
            _LOGGER.error(f"Error writing holding register {address}: {err}")
            raise UpdateFailed(f"Error writing register: {err}")
    
    def _write_holding_register_sync(self, address: int, value: int) -> bool:
        """Synchronous write to holding register."""
        try:
            if not self._client.connect():
                _LOGGER.error("Failed to connect to inverter for writing")
                return False
            
            success = self._client.write_holding_register(address, value)
            self._client.disconnect()
            
            return success
        except Exception as err:
            _LOGGER.error(f"Error writing holding register: {err}")
            if self._client:
                try:
                    self._client.disconnect()
                except Exception as disconnect_err:
                    _LOGGER.debug(f"Error during disconnect after write failure: {disconnect_err}")
            return False
    
    async def async_load_holding_registers(self) -> None:
        """Load holding registers into cache on startup."""
        register_map = self._get_register_map()
        if register_map not in REGISTER_MAPS:
            return
        
        holding_registers = REGISTER_MAPS[register_map].get("holding_registers", {})
        
        # Group consecutive registers for efficient reading
        if not holding_registers:
            return
        
        addresses = sorted(holding_registers.keys())
        if not addresses:
            return
        
        # Group consecutive addresses into chunks of up to 10 for efficient reading
        consecutive_chunks = []
        current_chunk = []
        for addr in addresses:
            if not current_chunk:
                current_chunk = [addr]
            elif addr == current_chunk[-1] + 1 and len(current_chunk) < 10:
                current_chunk.append(addr)
            else:
                consecutive_chunks.append(current_chunk)
                current_chunk = [addr]
        if current_chunk:
            consecutive_chunks.append(current_chunk)

        for chunk in consecutive_chunks:
            start_addr = chunk[0]
            count = len(chunk)
            try:
                await self.async_read_holding_registers(start_addr, count)
            except Exception as err:
                _LOGGER.debug(f"Could not read holding registers {start_addr}-{start_addr + count - 1}: {err}")