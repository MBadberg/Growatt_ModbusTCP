"""Select platform for Growatt Modbus integration."""
import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REGISTER_MAPS
from .coordinator import GrowattModbusCoordinator

_LOGGER = logging.getLogger(__name__)

# Selection options for different register types
SELECT_OPTIONS = {
    "priority_mode": {
        "options": ["Load First", "Battery First", "Grid First"],
        "values": [0, 1, 2],
    },
    "on_off": {
        "options": ["Off", "On"],
        "values": [0, 1],
    },
    "ac_charge_enable": {
        "options": ["Disabled", "Enabled"],
        "values": [0, 1],
    },
    "grid_charge_enable": {
        "options": ["Disabled", "Enabled"],
        "values": [0, 1],
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Growatt Modbus select entities."""
    coordinator: GrowattModbusCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    # Get register map for this inverter
    register_map_name = config_entry.data.get("register_map", "SPH_3000_10000")
    register_map = REGISTER_MAPS.get(register_map_name, {})
    holding_registers = register_map.get("holding_registers", {})
    
    entities = []
    
    # Create select entities for enum-type writable holding registers
    for address, register_info in holding_registers.items():
        if register_info.get("access") == "RW":
            register_name = register_info["name"]
            # Check if this register has predefined select options
            if register_name in SELECT_OPTIONS:
                entities.append(
                    GrowattModbusSelect(
                        coordinator=coordinator,
                        config_entry=config_entry,
                        register_address=address,
                        register_info=register_info,
                        select_config=SELECT_OPTIONS[register_name],
                    )
                )
    
    if entities:
        async_add_entities(entities)
        _LOGGER.info(f"Added {len(entities)} select entities")


class GrowattModbusSelect(CoordinatorEntity, SelectEntity):
    """Representation of a Growatt Modbus select entity."""

    def __init__(
        self,
        coordinator: GrowattModbusCoordinator,
        config_entry: ConfigEntry,
        register_address: int,
        register_info: dict,
        select_config: dict,
    ) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._register_address = register_address
        self._register_info = register_info
        self._select_config = select_config
        self._attr_name = f"{config_entry.data.get('name', 'Growatt')} {register_info['name'].replace('_', ' ').title()}"
        self._attr_unique_id = f"{config_entry.entry_id}_{register_info['name']}"
        self._attr_options = select_config["options"]
        
        # Set device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name=config_entry.data.get("name", "Growatt Inverter"),
            manufacturer="Growatt",
            model=config_entry.data.get("inverter_series", "Unknown"),
        )
        
        _LOGGER.debug(
            f"Created select entity: {self._attr_name} (address={register_address}, "
            f"options={self._attr_options})"
        )

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        try:
            # Try to read from coordinator data
            if hasattr(self.coordinator, "holding_register_cache"):
                raw_value = self.coordinator.holding_register_cache.get(self._register_address)
                if raw_value is not None:
                    # Map raw value to option string
                    values = self._select_config["values"]
                    options = self._select_config["options"]
                    if raw_value in values:
                        index = values.index(raw_value)
                        return options[index]
            
            return None
        except Exception as e:
            _LOGGER.error(f"Error getting option for {self._attr_name}: {e}")
            return None

    async def async_select_option(self, option: str) -> None:
        """Set the option."""
        try:
            # Map option string to raw value
            options = self._select_config["options"]
            values = self._select_config["values"]
            
            if option not in options:
                _LOGGER.error(f"Invalid option {option} for {self._attr_name}")
                return
            
            index = options.index(option)
            raw_value = values[index]
            
            _LOGGER.info(
                f"Setting {self._attr_name} to '{option}' (raw: {raw_value}) "
                f"at address {self._register_address}"
            )
            
            # Write to inverter via coordinator
            await self.coordinator.async_write_holding_register(
                self._register_address, raw_value
            )
            
            # Request immediate refresh
            await self.coordinator.async_request_refresh()
            
        except Exception as e:
            _LOGGER.error(f"Error setting {self._attr_name} to {option}: {e}")
            raise

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
