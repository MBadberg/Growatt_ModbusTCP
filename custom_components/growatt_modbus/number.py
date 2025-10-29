"""Number platform for Growatt Modbus integration."""
import logging

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, REGISTER_MAPS
from .coordinator import GrowattModbusCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Growatt Modbus number entities."""
    coordinator: GrowattModbusCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    # Get register map for this inverter
    register_map_name = config_entry.data.get("register_map", "SPH_3000_10000")
    register_map = REGISTER_MAPS.get(register_map_name, {})
    holding_registers = register_map.get("holding_registers", {})
    
    entities = []
    
    # Create number entities for writable holding registers
    for address, register_info in holding_registers.items():
        if register_info.get("access") == "RW":
            # Determine if this should be a number entity
            unit = register_info.get("unit", "")
            if unit in ["%", "h", "min", "V", "W", "A", ""] and "min" in register_info and "max" in register_info:
                entities.append(
                    GrowattModbusNumber(
                        coordinator=coordinator,
                        config_entry=config_entry,
                        register_address=address,
                        register_info=register_info,
                    )
                )
    
    if entities:
        async_add_entities(entities)
        _LOGGER.info(f"Added {len(entities)} number entities")


class GrowattModbusNumber(CoordinatorEntity, NumberEntity):
    """Representation of a Growatt Modbus number entity."""

    def __init__(
        self,
        coordinator: GrowattModbusCoordinator,
        config_entry: ConfigEntry,
        register_address: int,
        register_info: dict,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._register_address = register_address
        self._register_info = register_info
        self._attr_name = f"{config_entry.data.get('name', 'Growatt')} {register_info['name'].replace('_', ' ').title()}"
        self._attr_unique_id = f"{config_entry.entry_id}_{register_info['name']}"
        
        # Set number properties
        scale = register_info.get("scale", 1)
        self._attr_native_min_value = register_info.get("min", 0) * scale
        self._attr_native_max_value = register_info.get("max", 100) * scale
        self._attr_native_step = scale if scale < 1 else 1.0
        self._attr_mode = NumberMode.BOX
        
        # Set unit
        unit = register_info.get("unit", "")
        if unit == "%":
            self._attr_native_unit_of_measurement = PERCENTAGE
        elif unit:
            self._attr_native_unit_of_measurement = unit
        
        # Set device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            name=config_entry.data.get("name", "Growatt Inverter"),
            manufacturer="Growatt",
            model=config_entry.data.get("inverter_series", "Unknown"),
        )
        
        _LOGGER.debug(
            f"Created number entity: {self._attr_name} (address={register_address}, "
            f"min={self._attr_native_min_value}, max={self._attr_native_max_value})"
        )

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        try:
            # Try to read from coordinator data
            if hasattr(self.coordinator, "holding_register_cache"):
                raw_value = self.coordinator.holding_register_cache.get(self._register_address)
                if raw_value is not None:
                    scale = self._register_info.get("scale", 1)
                    return raw_value * scale
            
            # Fallback to None if not available
            return None
        except Exception as e:
            _LOGGER.error(f"Error getting value for {self._attr_name}: {e}")
            return None

    async def async_set_native_value(self, value: float) -> None:
        """Set the value."""
        try:
            # Convert to raw register value
            scale = self._register_info.get("scale", 1)
            raw_value = int(value / scale)
            
            _LOGGER.info(
                f"Setting {self._attr_name} to {value} (raw: {raw_value}) "
                f"at address {self._register_address}"
            )
            
            # Write to inverter via coordinator
            await self.coordinator.async_write_holding_register(
                self._register_address, raw_value
            )
            
            # Request immediate refresh
            await self.coordinator.async_request_refresh()
            
        except Exception as e:
            _LOGGER.error(f"Error setting {self._attr_name} to {value}: {e}")
            raise

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()
