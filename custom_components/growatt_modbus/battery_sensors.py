"""
Battery sensor definitions for hybrid/storage inverters (SPH, MOD series).
Add these to SENSOR_DEFINITIONS in sensor.py
"""

# Battery sensors for hybrid/storage models
BATTERY_SENSOR_DEFINITIONS = {
    # Battery Voltage/Current/Power
    "battery_voltage": {
        "name": "Battery Voltage",
        "icon": "mdi:battery-charging",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "attr": "battery_voltage",
    },
    "battery_current": {
        "name": "Battery Current",
        "icon": "mdi:current-dc",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "attr": "battery_current",
    },
    "battery_power": {
        "name": "Battery Power",
        "icon": "mdi:battery-charging-medium",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "battery_power",
    },
    
    # Battery State of Charge
    "battery_soc": {
        "name": "Battery State of Charge",
        "icon": "mdi:battery-medium",
        "device_class": SensorDeviceClass.BATTERY,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": PERCENTAGE,
        "attr": "battery_soc",
    },
    
    # Battery Temperature
    "battery_temp": {
        "name": "Battery Temperature",
        "icon": "mdi:thermometer",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
        "attr": "battery_temp",
    },
    
    # Battery Energy - Daily
    "battery_charge_today": {
        "name": "Battery Charge Today",
        "icon": "mdi:battery-arrow-up",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "battery_charge_today",
    },
    "battery_discharge_today": {
        "name": "Battery Discharge Today",
        "icon": "mdi:battery-arrow-down",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "battery_discharge_today",
    },
    
    # Battery Energy - Total
    "battery_charge_total": {
        "name": "Battery Charge Total",
        "icon": "mdi:battery-arrow-up",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "battery_charge_total",
    },
    "battery_discharge_total": {
        "name": "Battery Discharge Total",
        "icon": "mdi:battery-arrow-down",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "attr": "battery_discharge_total",
    },
}


# Three-phase sensor definitions for MID/MAX/MOD series
THREE_PHASE_SENSOR_DEFINITIONS = {
    # Phase R (Red)
    "ac_voltage_r": {
        "name": "AC Voltage Phase R",
        "icon": "mdi:lightning-bolt",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "attr": "ac_voltage_r",
    },
    "ac_current_r": {
        "name": "AC Current Phase R",
        "icon": "mdi:current-ac",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "attr": "ac_current_r",
    },
    "ac_power_r": {
        "name": "AC Power Phase R",
        "icon": "mdi:power-plug",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "ac_power_r",
    },
    
    # Phase S (Yellow)
    "ac_voltage_s": {
        "name": "AC Voltage Phase S",
        "icon": "mdi:lightning-bolt",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "attr": "ac_voltage_s",
    },
    "ac_current_s": {
        "name": "AC Current Phase S",
        "icon": "mdi:current-ac",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "attr": "ac_current_s",
    },
    "ac_power_s": {
        "name": "AC Power Phase S",
        "icon": "mdi:power-plug",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "ac_power_s",
    },
    
    # Phase T (Blue)
    "ac_voltage_t": {
        "name": "AC Voltage Phase T",
        "icon": "mdi:lightning-bolt",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricPotential.VOLT,
        "attr": "ac_voltage_t",
    },
    "ac_current_t": {
        "name": "AC Current Phase T",
        "icon": "mdi:current-ac",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfElectricCurrent.AMPERE,
        "attr": "ac_current_t",
    },
    "ac_power_t": {
        "name": "AC Power Phase T",
        "icon": "mdi:power-plug",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfPower.WATT,
        "attr": "ac_power_t",
    },
}


# Instructions for adding to sensor.py:
# 1. Add BATTERY_SENSOR_DEFINITIONS to SENSOR_DEFINITIONS dict
# 2. Add THREE_PHASE_SENSOR_DEFINITIONS to SENSOR_DEFINITIONS dict
# 3. Update const.py SENSOR_TYPES to include battery sensors in appropriate categories
# 4. Create register maps for SPH, MOD, MID, MAX series in const.py