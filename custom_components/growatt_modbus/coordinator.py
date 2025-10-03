"""Data update coordinator for Growatt Modbus Integration."""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    CONF_SLAVE_ID,
    CONF_CONNECTION_TYPE,
    CONF_DEVICE_PATH,
    CONF_BAUDRATE,
    CONF_REGISTER_MAP,
    REGISTER_MAPS,
)
from .growatt_modbus import GrowattModbus, GrowattData

_LOGGER = logging.getLogger(__name__)

# Map old register map names to new ones for migration
REGISTER_MAP_MIGRATION = {
    'MIN_10000_VARIANT_A': 'MIN_10000_TL_X_OFFICIAL',
    'MIN_10000_CORRECTED': 'MIN_10000_TL_X_OFFICIAL',
    'MIN_SERIES_STANDARD': 'MIN_10000_TL_X_OFFICIAL',
}


def test_connection(config: Dict[str, Any]) -> Dict[str, Any]:
    """Test connection to the Growatt inverter."""
    try:
        # Migrate old register map names
        register_map = config.get(CONF_REGISTER_MAP, 'MIN_10000_TL_X_OFFICIAL')
        register_map = REGISTER_MAP_MIGRATION.get(register_map, register_map)
        
        # Ensure register map exists
        if register_map not in REGISTER_MAPS:
            register_map = 'MIN_10000_TL_X_OFFICIAL'
        
        # Create the modbus client based on configuration
        if config[CONF_CONNECTION_TYPE] == "tcp":
            client = GrowattModbus(
                connection_type="tcp",
                host=config[CONF_HOST],
                port=config[CONF_PORT],
                slave_id=config[CONF_SLAVE_ID],
                register_map=register_map
            )
        else:
            client = GrowattModbus(
                connection_type="serial",
                device=config[CONF_DEVICE_PATH],
                baudrate=config[CONF_BAUDRATE],
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

    def _get_register_map(self) -> str:
        """Get register map with migration support."""
        register_map = self.config.get(CONF_REGISTER_MAP, 'MIN_10000_TL_X_OFFICIAL')
        
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
                "Unknown register map '%s', falling back to MIN_10000_TL_X_OFFICIAL",
                register_map
            )
            register_map = 'MIN_10000_TL_X_OFFICIAL'
        
        return register_map

    def _initialize_client(self):
        """Initialize the Growatt Modbus client."""
        try:
            register_map = self._get_register_map()
            
            if self.config[CONF_CONNECTION_TYPE] == "tcp":
                self._client = GrowattModbus(
                    connection_type="tcp",
                    host=self.config[CONF_HOST],
                    port=self.config[CONF_PORT],
                    slave_id=self.config[CONF_SLAVE_ID],
                    register_map=register_map
                )
            else:
                self._client = GrowattModbus(
                    connection_type="serial",
                    device=self.config[CONF_DEVICE_PATH],
                    baudrate=self.config[CONF_BAUDRATE],
                    slave_id=self.config[CONF_SLAVE_ID],
                    register_map=register_map
                )
                
            _LOGGER.info("Initialized Growatt client with register map: %s", register_map)
            
        except Exception as err:
            _LOGGER.error("Failed to initialize Growatt client: %s", err)
            self._client = None

    async def _async_update_data(self) -> GrowattData:
        """Fetch data from the Growatt inverter."""
        if self._client is None:
            raise UpdateFailed("Growatt client not initialized")

        try:
            # Run the blocking operations in executor
            data = await self.hass.async_add_executor_job(self._fetch_data)
            
            if data is None:
                # Inverter not responding (probably night time or powered off)
                # Keep last known data to prevent sensors going unavailable
                if self.data is not None:
                    _LOGGER.debug("Inverter not responding, keeping last known data (likely night time)")
                    return self.data
                else:
                    # First connection attempt failed
                    raise UpdateFailed("Failed to read data from inverter")
            
            # Update successful - record timestamp
            self.last_successful_update = datetime.now()
            return data
            
        except Exception as err:
            _LOGGER.error("Error fetching data from Growatt inverter: %s", err)
            # Keep last data if available
            if self.data is not None:
                _LOGGER.debug("Error fetching data, keeping last known data")
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