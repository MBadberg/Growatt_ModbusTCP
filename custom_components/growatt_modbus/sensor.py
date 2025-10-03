"""Sensor platform for Growatt Modbus Integration."""
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import GrowattModbusCoordinator

_LOGGER = logging.getLogger(__name__)


SENSOR_DEFINITIONS = {
    # Solar Input Sensors
    "pv1_voltage": {
        "name": "PV1 Voltage",
        "icon": "mdi:lightning-bolt",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "attr": "pv1_voltage",
    },
    "pv1_current": {
        "name": "PV1 Current", 
        "icon": "mdi:current-dc",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "attr": "pv1_current",
    },
    "pv1_power": {
        "name": "PV1 Power",
        "icon": "mdi:solar-panel",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "pv1_power",
    },
    "pv2_voltage": {
        "name": "PV2 Voltage",
        "icon": "mdi:lightning-bolt",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "attr": "pv2_voltage",
    },
    "pv2_current": {
        "name": "PV2 Current",
        "icon": "mdi:current-dc", 
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "attr": "pv2_current",
    },
    "pv2_power": {
        "name": "PV2 Power",
        "icon": "mdi:solar-panel",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "pv2_power",
    },
    "pv_total_power": {
        "name": "Solar Total Power",
        "icon": "mdi:solar-power",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "pv_total_power",
    },
    
    # AC Output Sensors
    "ac_voltage": {
        "name": "AC Voltage",
        "icon": "mdi:lightning-bolt",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "attr": "ac_voltage",
    },
    "ac_current": {
        "name": "AC Current",
        "icon": "mdi:current-ac",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "attr": "ac_current",
    },
    "ac_power": {
        "name": "AC Power",
        "icon": "mdi:power-plug",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "ac_power",
    },
    "ac_frequency": {
        "name": "AC Frequency",
        "icon": "mdi:sine-wave",
        "device_class": SensorDeviceClass.FREQUENCY,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfFrequency.HERTZ,
        "attr": "ac_frequency",
    },
    
    # Power Flow Sensors (storage/hybrid models or smart meter)
    "power_to_grid": {
        "name": "Power to Grid",
        "icon": "mdi:transmission-tower-export",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "power_to_grid",
        "condition": lambda data: data.power_to_grid > 0,
    },
    "power_to_load": {
        "name": "Power to Load",
        "icon": "mdi:home-lightning-bolt",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "power_to_load",
        "condition": lambda data: data.power_to_load > 0,
    },
    "power_to_user": {
        "name": "Power to User",
        "icon": "mdi:home-import-outline",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "power_to_user",
        "condition": lambda data: data.power_to_user > 0,
    },
    
    # Export/Import Split Sensors (calculated from power flow)
    "grid_export_power": {
        "name": "Grid Export Power",
        "icon": "mdi:transmission-tower-export",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "calculated",
    },
    "grid_import_power": {
        "name": "Grid Import Power",
        "icon": "mdi:transmission-tower-import", 
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "calculated",
    },
    "self_consumption": {
        "name": "Self Consumption",
        "icon": "mdi:home-lightning-bolt-outline",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "calculated",
    },
    "house_consumption": {
        "name": "House Consumption",
        "icon": "mdi:home-lightning-bolt",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "calculated",
    },
    
    # Energy Sensors
    "energy_today": {
        "name": "Energy Today",
        "icon": "mdi:calendar-today",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "energy_today",
    },
    "energy_total": {
        "name": "Energy Total",
        "icon": "mdi:counter",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "energy_total",
    },
    
    # Energy Breakdown (storage/hybrid models)
    "energy_to_grid_today": {
        "name": "Energy to Grid Today",
        "icon": "mdi:transmission-tower",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "energy_to_grid_today",
        "condition": lambda data: data.energy_to_grid_today > 0,
    },
    "energy_to_grid_total": {
        "name": "Energy to Grid Total",
        "icon": "mdi:transmission-tower",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "energy_to_grid_total",
        "condition": lambda data: data.energy_to_grid_total > 0,
    },
    "load_energy_today": {
        "name": "Load Energy Today",
        "icon": "mdi:home-lightning-bolt",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "load_energy_today",
        "condition": lambda data: data.load_energy_today > 0,
    },
    "load_energy_total": {
        "name": "Load Energy Total",
        "icon": "mdi:home-lightning-bolt",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "load_energy_total",
        "condition": lambda data: data.load_energy_total > 0,
    },
    
    # Temperature Sensors
    "inverter_temp": {
        "name": "Inverter Temperature",
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
        "attr": "inverter_temp",
    },
    "ipm_temp": {
        "name": "IPM Temperature",
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
        "attr": "ipm_temp",
        "condition": lambda data: data.ipm_temp > 0,
    },
    "boost_temp": {
        "name": "Boost Temperature",
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
        "attr": "boost_temp",
        "condition": lambda data: data.boost_temp > 0,
    },
    
    # System Sensors
    "status": {
        "name": "Status",
        "icon": "mdi:information",
        "attr": "status",
    },
    "derating_mode": {
        "name": "Derating Mode",
        "icon": "mdi:speedometer-slow",
        "attr": "derating_mode",
        "condition": lambda data: data.derating_mode > 0,
    },
    "fault_code": {
        "name": "Fault Code",
        "icon": "mdi:alert-circle",
        "attr": "fault_code",
        "condition": lambda data: data.fault_code > 0,
    },
    "warning_code": {
        "name": "Warning Code",
        "icon": "mdi:alert",
        "attr": "warning_code",
        "condition": lambda data: data.warning_code > 0,
    },
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Growatt Modbus sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    # Wait for first data to determine which sensors to create
    if coordinator.data is None:
        _LOGGER.warning("No data available from coordinator during sensor setup")
        return
    
    entities = []
    
    # Create sensors based on available data and conditions
    for sensor_key, sensor_def in SENSOR_DEFINITIONS.items():
        # Check if sensor should be created based on condition
        if "condition" in sensor_def:
            try:
                if not sensor_def["condition"](coordinator.data):
                    _LOGGER.debug("Skipping sensor %s - condition not met", sensor_key)
                    continue
            except (AttributeError, TypeError) as e:
                _LOGGER.debug("Skipping sensor %s - error checking condition: %s", sensor_key, e)
                continue
        
        entities.append(
            GrowattModbusSensor(
                coordinator,
                config_entry,
                sensor_key,
                sensor_def,
            )
        )
    
    async_add_entities(entities)


class GrowattModbusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Growatt Modbus sensor."""

    def __init__(
        self,
        coordinator: GrowattModbusCoordinator,
        config_entry: ConfigEntry,
        sensor_key: str,
        sensor_def: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._config_entry = config_entry
        self._sensor_key = sensor_key
        self._sensor_def = sensor_def
        self._attr_name = f"{config_entry.data['name']} {sensor_def['name']}"
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_key}"
        
        # Set sensor attributes based on definition
        if "device_class" in sensor_def:
            self._attr_device_class = sensor_def["device_class"]
        if "state_class" in sensor_def:
            self._attr_state_class = sensor_def["state_class"]
        if "unit" in sensor_def:
            self._attr_native_unit_of_measurement = sensor_def["unit"]
        if "icon" in sensor_def:
            self._attr_icon = sensor_def["icon"]

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return self.coordinator.device_info

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        
        data = self.coordinator.data
        
        # Special handling for calculated sensors
        if self._sensor_def.get("attr") == "calculated":
            if self._sensor_key == "grid_export_power":
                # Export = power flowing TO grid (positive direction)
                # Use power_to_grid if available (from official registers)
                export = getattr(data, "power_to_grid", 0)
                return round(max(0, export), 1)
                
            elif self._sensor_key == "grid_import_power":
                # Import = power flowing FROM grid (when solar < load)
                # Calculate as: house_consumption - solar_production (when positive)
                solar = getattr(data, "pv_total_power", 0)
                load = getattr(data, "power_to_load", 0)
                
                # If load data not available, can't calculate import
                if load == 0:
                    return 0
                
                # Import happens when load exceeds solar production
                import_power = max(0, load - solar)
                return round(import_power, 1)
                
            elif self._sensor_key == "self_consumption":
                # Self consumption = solar power used directly by house (not exported)
                # = min(solar_production, house_load)
                # OR = solar_production - grid_export
                solar = getattr(data, "pv_total_power", 0)
                export = getattr(data, "power_to_grid", 0)
                load = getattr(data, "power_to_load", 0)
                
                if export > 0:
                    # We have export data, use it
                    self_consumption = solar - export
                elif load > 0:
                    # We have load data, use it
                    self_consumption = min(solar, load)
                else:
                    # No power flow data, assume all solar is self-consumed
                    self_consumption = solar
                
                return round(max(0, self_consumption), 1)
                
            elif self._sensor_key == "house_consumption":
                # House consumption = total load
                # Prefer power_to_load from official registers
                load = getattr(data, "power_to_load", 0)
                
                # If not available, calculate as: solar + import - export
                if load == 0:
                    solar = getattr(data, "pv_total_power", 0)
                    export = getattr(data, "power_to_grid", 0)
                    # For basic calculation: if exporting, load = solar - export
                    # If importing, load = solar + import (but we don't have import directly)
                    if export > 0:
                        load = max(0, solar - export)
                    else:
                        load = solar
                
                return round(max(0, load), 1)
            
            return None
        
        # Regular sensor - get value from data attribute
        value = getattr(data, self._sensor_def["attr"], None)
        
        if value is None:
            return None
        
        # Apply transform function if defined
        if "transform" in self._sensor_def:
            value = self._sensor_def["transform"](value)
        
        # Special handling for status sensor
        if self._sensor_key == "status":
            from .const import STATUS_CODES
            status_info = STATUS_CODES.get(value, {"name": f"Unknown ({value})"})
            return status_info["name"]
        
        # Round numeric values to reasonable precision
        if isinstance(value, float):
            if self._sensor_def.get("unit") == UnitOfPower.WATT:
                return round(value, 1)
            elif self._sensor_def.get("unit") == UnitOfElectricPotential.VOLT:
                return round(value, 1)
            elif self._sensor_def.get("unit") == UnitOfElectricCurrent.AMPERE:
                return round(value, 2)
            elif self._sensor_def.get("unit") == UnitOfFrequency.HERTZ:
                return round(value, 2)
            elif self._sensor_def.get("unit") == UnitOfTemperature.CELSIUS:
                return round(value, 1)
            elif self._sensor_def.get("unit") == UnitOfEnergy.KILO_WATT_HOUR:
                return round(value, 2)
        
        return value

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        if self.coordinator.data is None:
            return None
        
        attributes = {}
        data = self.coordinator.data
        
        # Add last successful update time for status monitoring
        if self.coordinator.last_successful_update:
            attributes["last_successful_update"] = self.coordinator.last_successful_update.isoformat()
        
        # Add device information for main sensors
        if self._sensor_key in ["pv_total_power", "ac_power", "status"]:
            attributes.update({
                "firmware_version": data.firmware_version,
                "serial_number": data.serial_number,
                "register_map": self.coordinator.config.get("register_map", "Unknown"),
            })
        
        # Add power flow breakdown for export/import sensors
        if self._sensor_key == "grid_export_power":
            attributes["solar_production"] = round(getattr(data, "pv_total_power", 0), 1)
            attributes["house_load"] = round(getattr(data, "power_to_load", 0), 1)
            
        elif self._sensor_key == "grid_import_power":
            attributes["solar_production"] = round(getattr(data, "pv_total_power", 0), 1)
            attributes["house_load"] = round(getattr(data, "power_to_load", 0), 1)
            
        elif self._sensor_key == "self_consumption":
            solar = getattr(data, "pv_total_power", 0)
            export = getattr(data, "power_to_grid", 0)
            load = getattr(data, "power_to_load", 0)
            
            attributes["solar_production"] = round(solar, 1)
            attributes["grid_export"] = round(export, 1)
            attributes["house_load"] = round(load, 1)
            
            # Calculate percentage
            if solar > 0:
                self_consumption = max(0, solar - export) if export > 0 else min(solar, load)
                attributes["self_consumption_percentage"] = round((self_consumption / solar) * 100, 1)
        
        return attributes if attributes else None