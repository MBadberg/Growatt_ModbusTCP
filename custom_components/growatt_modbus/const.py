#!/usr/bin/env python3
"""
Growatt Inverter Register Definitions and Integration Constants
Modbus register mappings for Growatt MIN series inverters
Based on official Growatt Protocol V1.39 (2024.04.16)

REQUIREMENTS:
- Python 3.7+

Usage:
    from const import REGISTER_MAPS
    registers = REGISTER_MAPS['MIN_7000_10000TL_X']
"""

# Home Assistant Integration Constants
DOMAIN = "growatt_modbus"

# Configuration Constants
CONF_SLAVE_ID = "slave_id"
CONF_CONNECTION_TYPE = "connection_type"
CONF_DEVICE_PATH = "device_path"
CONF_BAUDRATE = "baudrate"
CONF_REGISTER_MAP = "register_map"
CONF_INVERTER_SERIES = "inverter_series"
CONF_INVERT_GRID_POWER = "invert_grid_power"  # NEW: For reversed CT clamps

# Default Values
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1
DEFAULT_BAUDRATE = 9600

# Sensor Type Classifications for Offline Behavior
SENSOR_TYPES = {
    # Power sensors - should go to 0 when offline
    'power': [
        'pv1_power', 'pv2_power', 'pv3_power', 'pv_total_power',
        'ac_power', 'grid_power', 'grid_export_power', 'grid_import_power',
        'power_to_grid', 'power_to_load', 'power_to_user',
        'self_consumption', 'house_consumption',
        # Battery power sensors
        'battery_power', 'battery_charge_power', 'battery_discharge_power',
        # Three-phase power sensors
        'ac_power_r', 'ac_power_s', 'ac_power_t',
    ],
    
    # Daily total sensors - retain until midnight, then reset
    'daily_total': [
        'energy_today', 'energy_to_grid_today', 'grid_import_energy_today',
        'load_energy_today', 'energy_to_user_today', 'grid_energy_today',
        # Battery daily sensors
        'battery_charge_today', 'battery_discharge_today',
    ],
    
    # Lifetime total sensors - always retain last value
    'lifetime_total': [
        'energy_total', 'energy_to_grid_total', 'grid_import_energy_total',
        'load_energy_total', 'energy_to_user_total', 'grid_energy_total',
        # Battery lifetime sensors
        'battery_charge_total', 'battery_discharge_total',
    ],
    
    # Diagnostic sensors - go unavailable when offline
    'diagnostic': [
        'pv1_voltage', 'pv1_current', 'pv2_voltage', 'pv2_current',
        'pv3_voltage', 'pv3_current', 'ac_voltage', 'ac_current',
        'ac_frequency', 'inverter_temp', 'ipm_temp', 'boost_temp',
        'self_consumption_percentage',
        # Battery diagnostic sensors
        'battery_voltage', 'battery_current', 'battery_soc', 'battery_temp',
        # Three-phase diagnostic sensors
        'ac_voltage_r', 'ac_voltage_s', 'ac_voltage_t',
        'ac_current_r', 'ac_current_s', 'ac_current_t',
    ],
    
    # Status sensors - show "offline" when not responding
    'status': ['status', 'derating_mode', 'fault_code', 'warning_code', 'priority_mode', 'battery_derating_mode'],
}

# Sensor offline behavior mapping
SENSOR_OFFLINE_BEHAVIOR = {
    'power': 0,              # Power sensors go to 0W
    'daily_total': 'retain', # Daily totals retain until midnight
    'lifetime_total': 'retain', # Lifetime totals always retain
    'diagnostic': None,      # Diagnostic sensors go unavailable
    'status': 'offline',     # Status shows "offline"
}

def get_sensor_type(sensor_key: str) -> str:
    """Get the sensor type for a given sensor key."""
    for sensor_type, sensors in SENSOR_TYPES.items():
        if sensor_key in sensors:
            return sensor_type
    return 'diagnostic'  # Default to diagnostic if not found

# MIN-3000-6000TL-X Series (2 PV strings, single phase)
MIN_3000_6000TL_X = {
    'name': 'MIN-3000-6000TL-X',
    'description': '2 PV string single-phase inverter (3-6kW)',
    'notes': 'Uses 3000-3124 register range. No PV3 string.',
    'input_registers': {
        # System Status
        3000: {'name': 'inverter_status', 'scale': 1, 'unit': '', 'desc': '0=Waiting, 1=Normal, 3=Fault'},
        
        # PV Total Power (32-bit)
        3001: {'name': 'pv_total_power_high', 'scale': 1, 'unit': '', 'desc': 'Total PV power HIGH word', 'pair': 3002},
        3002: {'name': 'pv_total_power_low', 'scale': 1, 'unit': '', 'desc': 'Total PV power LOW word', 'pair': 3001, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 1
        3003: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'PV1 DC voltage'},
        3004: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A', 'desc': 'PV1 DC current'},
        3005: {'name': 'pv1_power_high', 'scale': 1, 'unit': '', 'desc': 'PV1 power HIGH word', 'pair': 3006},
        3006: {'name': 'pv1_power_low', 'scale': 1, 'unit': '', 'desc': 'PV1 power LOW word', 'pair': 3005, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 2
        3007: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'PV2 DC voltage'},
        3008: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A', 'desc': 'PV2 DC current'},
        3009: {'name': 'pv2_power_high', 'scale': 1, 'unit': '', 'desc': 'PV2 power HIGH word', 'pair': 3010},
        3010: {'name': 'pv2_power_low', 'scale': 1, 'unit': '', 'desc': 'PV2 power LOW word', 'pair': 3009, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # AC Output
        3025: {'name': 'ac_frequency', 'scale': 0.01, 'unit': 'Hz', 'desc': 'AC frequency'},
        3026: {'name': 'ac_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'AC voltage'},
        3027: {'name': 'ac_current', 'scale': 0.1, 'unit': 'A', 'desc': 'AC current'},
        3028: {'name': 'ac_power_high', 'scale': 1, 'unit': '', 'desc': 'AC power HIGH', 'pair': 3029},
        3029: {'name': 'ac_power_low', 'scale': 1, 'unit': '', 'desc': 'AC power LOW', 'pair': 3028, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Power Flow - Grid can be positive (export) or negative (import)
        3041: {'name': 'power_to_user_high', 'scale': 1, 'unit': '', 'desc': 'Forward power HIGH', 'pair': 3042},
        3042: {'name': 'power_to_user_low', 'scale': 1, 'unit': '', 'desc': 'Forward power LOW', 'pair': 3041, 'combined_scale': 0.1, 'combined_unit': 'W'},
        3043: {'name': 'power_to_grid_high', 'scale': 1, 'unit': '', 'desc': 'Grid power HIGH (signed)', 'pair': 3044},
        3044: {'name': 'power_to_grid_low', 'scale': 1, 'unit': '', 'desc': 'Grid power LOW (signed)', 'pair': 3043, 'combined_scale': 0.1, 'combined_unit': 'W', 'signed': True},
        3045: {'name': 'power_to_load_high', 'scale': 1, 'unit': '', 'desc': 'Load power HIGH', 'pair': 3046},
        3046: {'name': 'power_to_load_low', 'scale': 1, 'unit': '', 'desc': 'Load power LOW', 'pair': 3045, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Energy Today (32-bit)
        3049: {'name': 'energy_today_high', 'scale': 1, 'unit': '', 'desc': 'Today energy HIGH', 'pair': 3050},
        3050: {'name': 'energy_today_low', 'scale': 1, 'unit': '', 'desc': 'Today energy LOW', 'pair': 3049, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Energy Total (32-bit)
        3051: {'name': 'energy_total_high', 'scale': 1, 'unit': '', 'desc': 'Total energy HIGH', 'pair': 3052},
        3052: {'name': 'energy_total_low', 'scale': 1, 'unit': '', 'desc': 'Total energy LOW', 'pair': 3051, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Energy Breakdown
        3067: {'name': 'energy_to_user_today_high', 'scale': 1, 'unit': '', 'pair': 3068},
        3068: {'name': 'energy_to_user_today_low', 'scale': 1, 'unit': '', 'pair': 3067, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3071: {'name': 'energy_to_grid_today_high', 'scale': 1, 'unit': '', 'pair': 3072},
        3072: {'name': 'energy_to_grid_today_low', 'scale': 1, 'unit': '', 'pair': 3071, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3075: {'name': 'load_energy_today_high', 'scale': 1, 'unit': '', 'pair': 3076},
        3076: {'name': 'load_energy_today_low', 'scale': 1, 'unit': '', 'pair': 3075, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Diagnostics
        3086: {'name': 'derating_mode', 'scale': 1, 'unit': '', 'desc': 'Derating status'},
        3092: {'name': 'bus_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'DC bus voltage'},
        
        # Temperatures
        3093: {'name': 'inverter_temp', 'scale': 0.1, 'unit': '°C', 'desc': 'Inverter temperature'},
        3094: {'name': 'ipm_temp', 'scale': 0.1, 'unit': '°C', 'desc': 'IPM temperature'},
        3095: {'name': 'boost_temp', 'scale': 0.1, 'unit': '°C', 'desc': 'Boost temperature'},
        
        # Fault Codes
        3105: {'name': 'fault_code', 'scale': 1, 'unit': '', 'desc': 'Main fault code'},
        3106: {'name': 'warning_code', 'scale': 1, 'unit': '', 'desc': 'Main warning code'},
    },
    'holding_registers': {
        0: {'name': 'on_off', 'scale': 1, 'unit': '', 'access': 'RW', 'desc': '0=Off, 1=On'},
        3: {'name': 'active_power_rate', 'scale': 1, 'unit': '%', 'access': 'RW', 'desc': 'Max output power %'},
        30: {'name': 'modbus_address', 'scale': 1, 'unit': '', 'access': 'RW', 'desc': 'Modbus address 1-254'},
    }
}

# MIN-7000-10000TL-X Series (3 PV strings, single phase) - YOUR WORKING CONFIG
MIN_7000_10000TL_X = {
    'name': 'MIN-7000-10000TL-X',
    'description': '3 PV string single-phase inverter (7-10kW)',
    'notes': 'Uses 3000-3124 register range. Includes PV3 string.',
    'input_registers': {
        # System Status
        3000: {'name': 'inverter_status', 'scale': 1, 'unit': '', 'desc': '0=Waiting, 1=Normal, 3=Fault'},
        
        # PV Total Power (32-bit)
        3001: {'name': 'pv_total_power_high', 'scale': 1, 'unit': '', 'desc': 'Total PV power HIGH word', 'pair': 3002},
        3002: {'name': 'pv_total_power_low', 'scale': 1, 'unit': '', 'desc': 'Total PV power LOW word', 'pair': 3001, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 1
        3003: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'PV1 DC voltage'},
        3004: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A', 'desc': 'PV1 DC current'},
        3005: {'name': 'pv1_power_high', 'scale': 1, 'unit': '', 'desc': 'PV1 power HIGH word', 'pair': 3006},
        3006: {'name': 'pv1_power_low', 'scale': 1, 'unit': '', 'desc': 'PV1 power LOW word', 'pair': 3005, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 2
        3007: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'PV2 DC voltage'},
        3008: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A', 'desc': 'PV2 DC current'},
        3009: {'name': 'pv2_power_high', 'scale': 1, 'unit': '', 'desc': 'PV2 power HIGH word', 'pair': 3010},
        3010: {'name': 'pv2_power_low', 'scale': 1, 'unit': '', 'desc': 'PV2 power LOW word', 'pair': 3009, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 3
        3011: {'name': 'pv3_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'PV3 DC voltage'},
        3012: {'name': 'pv3_current', 'scale': 0.1, 'unit': 'A', 'desc': 'PV3 DC current'},
        3013: {'name': 'pv3_power_high', 'scale': 1, 'unit': '', 'desc': 'PV3 power HIGH word', 'pair': 3014},
        3014: {'name': 'pv3_power_low', 'scale': 1, 'unit': '', 'desc': 'PV3 power LOW word', 'pair': 3013, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # System Output Power (32-bit)
        3019: {'name': 'system_output_power_high', 'scale': 1, 'unit': '', 'desc': 'System output power HIGH', 'pair': 3020},
        3020: {'name': 'system_output_power_low', 'scale': 1, 'unit': '', 'desc': 'System output power LOW', 'pair': 3019, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Reactive Power (32-bit)
        3021: {'name': 'reactive_power_high', 'scale': 1, 'unit': '', 'desc': 'Reactive power HIGH', 'pair': 3022},
        3022: {'name': 'reactive_power_low', 'scale': 1, 'unit': '', 'desc': 'Reactive power LOW', 'pair': 3021, 'combined_scale': 0.1, 'combined_unit': 'var'},
        
        # Output Power (32-bit)
        3023: {'name': 'output_power_high', 'scale': 1, 'unit': '', 'desc': 'Output power HIGH', 'pair': 3024},
        3024: {'name': 'output_power_low', 'scale': 1, 'unit': '', 'desc': 'Output power LOW', 'pair': 3023, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # AC Output (Inverter Output - NOT Grid!)
        3025: {'name': 'ac_frequency', 'scale': 0.01, 'unit': 'Hz', 'desc': 'Inverter AC output frequency'},
        3026: {'name': 'ac_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'Inverter AC output voltage'},
        3027: {'name': 'ac_current', 'scale': 0.1, 'unit': 'A', 'desc': 'Inverter AC output current'},
        3028: {'name': 'ac_power_high', 'scale': 1, 'unit': '', 'desc': 'AC power HIGH', 'pair': 3029},
        3029: {'name': 'ac_power_low', 'scale': 1, 'unit': '', 'desc': 'AC power LOW', 'pair': 3028, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Power Flow (32-bit pairs) - Grid power is SIGNED (positive=export, negative=import)
        3041: {'name': 'power_to_user_high', 'scale': 1, 'unit': '', 'desc': 'Forward power HIGH', 'pair': 3042},
        3042: {'name': 'power_to_user_low', 'scale': 1, 'unit': '', 'desc': 'Forward power LOW', 'pair': 3041, 'combined_scale': 0.1, 'combined_unit': 'W'},
        3043: {'name': 'power_to_grid_high', 'scale': 1, 'unit': '', 'desc': 'Grid power HIGH (signed: +export, -import)', 'pair': 3044},
        3044: {'name': 'power_to_grid_low', 'scale': 1, 'unit': '', 'desc': 'Grid power LOW (signed: +export, -import)', 'pair': 3043, 'combined_scale': 0.1, 'combined_unit': 'W', 'signed': True},
        3045: {'name': 'power_to_load_high', 'scale': 1, 'unit': '', 'desc': 'Load power HIGH', 'pair': 3046},
        3046: {'name': 'power_to_load_low', 'scale': 1, 'unit': '', 'desc': 'Load power LOW', 'pair': 3045, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Operating Time (32-bit)
        3047: {'name': 'time_total_high', 'scale': 1, 'unit': '', 'desc': 'Total time HIGH', 'pair': 3048},
        3048: {'name': 'time_total_low', 'scale': 1, 'unit': '', 'desc': 'Total time LOW', 'pair': 3047, 'combined_scale': 0.5, 'combined_unit': 's'},
        
        # Energy Today (32-bit)
        3049: {'name': 'energy_today_high', 'scale': 1, 'unit': '', 'desc': 'Today energy HIGH', 'pair': 3050},
        3050: {'name': 'energy_today_low', 'scale': 1, 'unit': '', 'desc': 'Today energy LOW', 'pair': 3049, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Energy Total (32-bit)
        3051: {'name': 'energy_total_high', 'scale': 1, 'unit': '', 'desc': 'Total energy HIGH', 'pair': 3052},
        3052: {'name': 'energy_total_low', 'scale': 1, 'unit': '', 'desc': 'Total energy LOW', 'pair': 3051, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Energy Breakdown (32-bit pairs)
        3067: {'name': 'energy_to_user_today_high', 'scale': 1, 'unit': '', 'pair': 3068},
        3068: {'name': 'energy_to_user_today_low', 'scale': 1, 'unit': '', 'pair': 3067, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3069: {'name': 'energy_to_user_total_high', 'scale': 1, 'unit': '', 'pair': 3070},
        3070: {'name': 'energy_to_user_total_low', 'scale': 1, 'unit': '', 'pair': 3069, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3071: {'name': 'energy_to_grid_today_high', 'scale': 1, 'unit': '', 'pair': 3072},
        3072: {'name': 'energy_to_grid_today_low', 'scale': 1, 'unit': '', 'pair': 3071, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3073: {'name': 'energy_to_grid_total_high', 'scale': 1, 'unit': '', 'pair': 3074},
        3074: {'name': 'energy_to_grid_total_low', 'scale': 1, 'unit': '', 'pair': 3073, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3075: {'name': 'load_energy_today_high', 'scale': 1, 'unit': '', 'pair': 3076},
        3076: {'name': 'load_energy_today_low', 'scale': 1, 'unit': '', 'pair': 3075, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3077: {'name': 'load_energy_total_high', 'scale': 1, 'unit': '', 'pair': 3078},
        3078: {'name': 'load_energy_total_low', 'scale': 1, 'unit': '', 'pair': 3077, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Diagnostics
        3086: {'name': 'derating_mode', 'scale': 1, 'unit': '', 'desc': 'Derating status'},
        3087: {'name': 'pv_iso', 'scale': 1, 'unit': 'kΩ', 'desc': 'PV isolation resistance'},
        3088: {'name': 'dci_r', 'scale': 0.1, 'unit': 'mA', 'desc': 'DC injection R phase'},
        3091: {'name': 'gfci', 'scale': 1, 'unit': 'mA', 'desc': 'Ground fault current'},
        3092: {'name': 'bus_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'DC bus voltage'},
        
        # Temperatures
        3093: {'name': 'inverter_temp', 'scale': 0.1, 'unit': '°C', 'desc': 'Inverter temperature'},
        3094: {'name': 'ipm_temp', 'scale': 0.1, 'unit': '°C', 'desc': 'IPM temperature'},
        3095: {'name': 'boost_temp', 'scale': 0.1, 'unit': '°C', 'desc': 'Boost temperature'},
        3097: {'name': 'comms_board_temp', 'scale': 0.1, 'unit': '°C', 'desc': 'Comms board temperature'},
        
        # Fault Codes
        3105: {'name': 'fault_code', 'scale': 1, 'unit': '', 'desc': 'Main fault code'},
        3106: {'name': 'warning_code', 'scale': 1, 'unit': '', 'desc': 'Main warning code'},
        3107: {'name': 'fault_subcode', 'scale': 1, 'unit': '', 'desc': 'Fault subcode'},
        3108: {'name': 'warning_subcode', 'scale': 1, 'unit': '', 'desc': 'Warning subcode'},
    },
    'holding_registers': {
        0: {'name': 'on_off', 'scale': 1, 'unit': '', 'access': 'RW', 'desc': '0=Off, 1=On'},
        3: {'name': 'active_power_rate', 'scale': 1, 'unit': '%', 'access': 'RW', 'desc': 'Max output power %'},
        15: {'name': 'lcd_language', 'scale': 1, 'unit': '', 'access': 'RW'},
        22: {'name': 'baud_rate', 'scale': 1, 'unit': '', 'access': 'RW', 'desc': '0=9600, 1=38400'},
        30: {'name': 'modbus_address', 'scale': 1, 'unit': '', 'access': 'RW', 'desc': 'Modbus address 1-254'},
        45: {'name': 'sys_year', 'scale': 1, 'unit': '', 'access': 'RW'},
        46: {'name': 'sys_month', 'scale': 1, 'unit': '', 'access': 'RW'},
        47: {'name': 'sys_day', 'scale': 1, 'unit': '', 'access': 'RW'},
        48: {'name': 'sys_hour', 'scale': 1, 'unit': '', 'access': 'RW'},
        49: {'name': 'sys_min', 'scale': 1, 'unit': '', 'access': 'RW'},
        50: {'name': 'sys_sec', 'scale': 1, 'unit': '', 'access': 'RW'},
    }
}

# TL3-X MID Series (Three-phase, 15-25kW)
MID_15000_25000TL3_X = {
    'name': 'MID-15000-25000TL3-X',
    'description': 'Three-phase commercial inverter (15-25kW)',
    'notes': 'Uses 0-124, 125-249 register range. Three-phase output.',
    'input_registers': {
        # System Status
        0: {'name': 'inverter_status', 'scale': 1, 'unit': '', 'desc': '0=Waiting, 1=Normal, 3=Fault'},
        
        # PV Totals
        1: {'name': 'pv_total_power_high', 'scale': 1, 'unit': '', 'pair': 2},
        2: {'name': 'pv_total_power_low', 'scale': 1, 'unit': '', 'pair': 1, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 1
        3: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V'},
        4: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A'},
        5: {'name': 'pv1_power_high', 'scale': 1, 'unit': '', 'pair': 6},
        6: {'name': 'pv1_power_low', 'scale': 1, 'unit': '', 'pair': 5, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 2
        7: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V'},
        8: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A'},
        9: {'name': 'pv2_power_high', 'scale': 1, 'unit': '', 'pair': 10},
        10: {'name': 'pv2_power_low', 'scale': 1, 'unit': '', 'pair': 9, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Output Power
        35: {'name': 'output_power_high', 'scale': 1, 'unit': '', 'pair': 36},
        36: {'name': 'output_power_low', 'scale': 1, 'unit': '', 'pair': 35, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Grid Frequency
        37: {'name': 'grid_frequency', 'scale': 0.01, 'unit': 'Hz'},
        
        # Phase R (L1)
        38: {'name': 'grid_voltage_r', 'scale': 0.1, 'unit': 'V', 'desc': 'Phase R voltage'},
        39: {'name': 'grid_current_r', 'scale': 0.1, 'unit': 'A', 'desc': 'Phase R current'},
        40: {'name': 'grid_power_r_high', 'scale': 1, 'unit': '', 'pair': 41},
        41: {'name': 'grid_power_r_low', 'scale': 1, 'unit': '', 'pair': 40, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Phase S (L2)
        42: {'name': 'grid_voltage_s', 'scale': 0.1, 'unit': 'V', 'desc': 'Phase S voltage'},
        43: {'name': 'grid_current_s', 'scale': 0.1, 'unit': 'A', 'desc': 'Phase S current'},
        44: {'name': 'grid_power_s_high', 'scale': 1, 'unit': '', 'pair': 45},
        45: {'name': 'grid_power_s_low', 'scale': 1, 'unit': '', 'pair': 44, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Phase T (L3)
        46: {'name': 'grid_voltage_t', 'scale': 0.1, 'unit': 'V', 'desc': 'Phase T voltage'},
        47: {'name': 'grid_current_t', 'scale': 0.1, 'unit': 'A', 'desc': 'Phase T current'},
        48: {'name': 'grid_power_t_high', 'scale': 1, 'unit': '', 'pair': 49},
        49: {'name': 'grid_power_t_low', 'scale': 1, 'unit': '', 'pair': 48, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Line voltages
        50: {'name': 'grid_voltage_rs', 'scale': 0.1, 'unit': 'V', 'desc': 'Line voltage R-S'},
        51: {'name': 'grid_voltage_st', 'scale': 0.1, 'unit': 'V', 'desc': 'Line voltage S-T'},
        52: {'name': 'grid_voltage_tr', 'scale': 0.1, 'unit': 'V', 'desc': 'Line voltage T-R'},
        
        # Energy
        53: {'name': 'energy_today_high', 'scale': 1, 'unit': '', 'pair': 54},
        54: {'name': 'energy_today_low', 'scale': 1, 'unit': '', 'pair': 53, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        55: {'name': 'energy_total_high', 'scale': 1, 'unit': '', 'pair': 56},
        56: {'name': 'energy_total_low', 'scale': 1, 'unit': '', 'pair': 55, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Temperatures
        93: {'name': 'inverter_temp', 'scale': 0.1, 'unit': '°C'},
        94: {'name': 'ipm_temp', 'scale': 0.1, 'unit': '°C'},
        95: {'name': 'boost_temp', 'scale': 0.1, 'unit': '°C'},
        
        # Status
        100: {'name': 'power_factor', 'scale': 1, 'unit': ''},
        104: {'name': 'derating_mode', 'scale': 1, 'unit': ''},
        105: {'name': 'fault_code', 'scale': 1, 'unit': ''},
        112: {'name': 'warning_code', 'scale': 1, 'unit': ''},
    },
    'holding_registers': {
        0: {'name': 'on_off', 'scale': 1, 'unit': '', 'access': 'RW'},
        3: {'name': 'active_power_rate', 'scale': 1, 'unit': '%', 'access': 'RW'},
        30: {'name': 'modbus_address', 'scale': 1, 'unit': '', 'access': 'RW'},
    }
}

# SPH Hybrid Series (Storage with battery)
SPH_3000_10000 = {
    'name': 'SPH-3000-10000',
    'description': 'Hybrid inverter with battery storage (3-10kW)',
    'notes': 'Uses 0-124, 1000-1124 register ranges. Includes battery management.',
    'input_registers': {
        # ============================================================================
        # BASE RANGE 0-124: PV Input and AC Output (same as MIN series)
        # ============================================================================
        
        # System Status
        0: {'name': 'inverter_status', 'scale': 1, 'unit': '', 'desc': '0=Waiting, 1=Normal, 3=Fault'},
        
        # PV Total Power (32-bit)
        1: {'name': 'pv_total_power_high', 'scale': 1, 'unit': '', 'desc': 'Total PV power HIGH word', 'pair': 2},
        2: {'name': 'pv_total_power_low', 'scale': 1, 'unit': '', 'desc': 'Total PV power LOW word', 'pair': 1, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 1
        3: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'PV1 DC voltage'},
        4: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A', 'desc': 'PV1 DC current'},
        5: {'name': 'pv1_power_high', 'scale': 1, 'unit': '', 'desc': 'PV1 power HIGH word', 'pair': 6},
        6: {'name': 'pv1_power_low', 'scale': 1, 'unit': '', 'desc': 'PV1 power LOW word', 'pair': 5, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 2
        7: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'PV2 DC voltage'},
        8: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A', 'desc': 'PV2 DC current'},
        9: {'name': 'pv2_power_high', 'scale': 1, 'unit': '', 'desc': 'PV2 power HIGH word', 'pair': 10},
        10: {'name': 'pv2_power_low', 'scale': 1, 'unit': '', 'desc': 'PV2 power LOW word', 'pair': 9, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # AC Output
        37: {'name': 'ac_frequency', 'scale': 0.01, 'unit': 'Hz', 'desc': 'AC frequency'},
        38: {'name': 'ac_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'AC voltage'},
        39: {'name': 'ac_current', 'scale': 0.1, 'unit': 'A', 'desc': 'AC current'},
        40: {'name': 'ac_power_high', 'scale': 1, 'unit': '', 'desc': 'AC power HIGH', 'pair': 41},
        41: {'name': 'ac_power_low', 'scale': 1, 'unit': '', 'desc': 'AC power LOW', 'pair': 40, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Energy
        53: {'name': 'energy_today_high', 'scale': 1, 'unit': '', 'desc': 'Today energy HIGH', 'pair': 54},
        54: {'name': 'energy_today_low', 'scale': 1, 'unit': '', 'desc': 'Today energy LOW', 'pair': 53, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        55: {'name': 'energy_total_high', 'scale': 1, 'unit': '', 'desc': 'Total energy HIGH', 'pair': 56},
        56: {'name': 'energy_total_low', 'scale': 1, 'unit': '', 'desc': 'Total energy LOW', 'pair': 55, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Temperatures
        93: {'name': 'inverter_temp', 'scale': 0.1, 'unit': '°C'},
        
        # Status
        105: {'name': 'fault_code', 'scale': 1, 'unit': ''},
        112: {'name': 'warning_code', 'scale': 1, 'unit': ''},
        
        # ============================================================================
        # STORAGE RANGE 1000-1124: Battery and Power Flow
        # ============================================================================
        
        # System Work Mode
        1000: {'name': 'system_work_mode', 'scale': 1, 'unit': '', 'desc': 'Work mode'},
        
        # Battery Discharge/Charge Power
        1009: {'name': 'discharge_power_high', 'scale': 1, 'unit': '', 'pair': 1010},
        1010: {'name': 'discharge_power_low', 'scale': 1, 'unit': '', 'pair': 1009, 'combined_scale': 0.1, 'combined_unit': 'W'},
        1011: {'name': 'charge_power_high', 'scale': 1, 'unit': '', 'pair': 1012},
        1012: {'name': 'charge_power_low', 'scale': 1, 'unit': '', 'pair': 1011, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Battery State
        1013: {'name': 'battery_voltage', 'scale': 0.1, 'unit': 'V'},
        1014: {'name': 'battery_soc', 'scale': 1, 'unit': '%'},
        1040: {'name': 'battery_temp', 'scale': 0.1, 'unit': '°C'},
        
        # Power Flow
        1015: {'name': 'power_to_user_high', 'scale': 1, 'unit': '', 'pair': 1016},
        1016: {'name': 'power_to_user_low', 'scale': 1, 'unit': '', 'pair': 1015, 'combined_scale': 0.1, 'combined_unit': 'W'},
        1021: {'name': 'power_to_load_high', 'scale': 1, 'unit': '', 'pair': 1022},
        1022: {'name': 'power_to_load_low', 'scale': 1, 'unit': '', 'pair': 1021, 'combined_scale': 0.1, 'combined_unit': 'W'},
        1029: {'name': 'power_to_grid_high', 'scale': 1, 'unit': '', 'pair': 1030},
        1030: {'name': 'power_to_grid_low', 'scale': 1, 'unit': '', 'pair': 1029, 'combined_scale': 0.1, 'combined_unit': 'W', 'signed': True},
        
        # Energy Breakdown
        1044: {'name': 'energy_to_user_today_high', 'scale': 1, 'unit': '', 'pair': 1045},
        1045: {'name': 'energy_to_user_today_low', 'scale': 1, 'unit': '', 'pair': 1044, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1046: {'name': 'energy_to_user_total_high', 'scale': 1, 'unit': '', 'pair': 1047},
        1047: {'name': 'energy_to_user_total_low', 'scale': 1, 'unit': '', 'pair': 1046, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1048: {'name': 'energy_to_grid_today_high', 'scale': 1, 'unit': '', 'pair': 1049},
        1049: {'name': 'energy_to_grid_today_low', 'scale': 1, 'unit': '', 'pair': 1048, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1050: {'name': 'energy_to_grid_total_high', 'scale': 1, 'unit': '', 'pair': 1051},
        1051: {'name': 'energy_to_grid_total_low', 'scale': 1, 'unit': '', 'pair': 1050, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1052: {'name': 'discharge_energy_today_high', 'scale': 1, 'unit': '', 'pair': 1053},
        1053: {'name': 'discharge_energy_today_low', 'scale': 1, 'unit': '', 'pair': 1052, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1054: {'name': 'discharge_energy_total_high', 'scale': 1, 'unit': '', 'pair': 1055},
        1055: {'name': 'discharge_energy_total_low', 'scale': 1, 'unit': '', 'pair': 1054, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1056: {'name': 'charge_energy_today_high', 'scale': 1, 'unit': '', 'pair': 1057},
        1057: {'name': 'charge_energy_today_low', 'scale': 1, 'unit': '', 'pair': 1056, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1058: {'name': 'charge_energy_total_high', 'scale': 1, 'unit': '', 'pair': 1059},
        1059: {'name': 'charge_energy_total_low', 'scale': 1, 'unit': '', 'pair': 1058, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1060: {'name': 'load_energy_today_high', 'scale': 1, 'unit': '', 'pair': 1061},
        1061: {'name': 'load_energy_today_low', 'scale': 1, 'unit': '', 'pair': 1060, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1062: {'name': 'load_energy_total_high', 'scale': 1, 'unit': '', 'pair': 1063},
        1063: {'name': 'load_energy_total_low', 'scale': 1, 'unit': '', 'pair': 1062, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
    },
    'holding_registers': {
        0: {'name': 'on_off', 'scale': 1, 'unit': '', 'access': 'RW'},
        1008: {'name': 'system_enable', 'scale': 1, 'unit': '', 'access': 'RW'},
        1044: {'name': 'priority', 'scale': 1, 'unit': '', 'access': 'RW', 'desc': '0=Load, 1=Battery, 2=Grid'},
    }
}

# MAX Series (Commercial Three-phase, 50-125kW)
MAX_50000_125000TL3_X = {
    'name': 'MAX-50000-125000TL3-X',
    'description': 'Commercial three-phase inverter (50-125kW)',
    'notes': 'Uses 0-124, 125-249, 875-999 register ranges. High power commercial.',
    'input_registers': {
        # System Status
        0: {'name': 'inverter_status', 'scale': 1, 'unit': '', 'desc': '0=Waiting, 1=Normal, 3=Fault'},
        
        # PV Totals
        1: {'name': 'pv_total_power_high', 'scale': 1, 'unit': '', 'pair': 2},
        2: {'name': 'pv_total_power_low', 'scale': 1, 'unit': '', 'pair': 1, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 1
        3: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V'},
        4: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A'},
        5: {'name': 'pv1_power_high', 'scale': 1, 'unit': '', 'pair': 6},
        6: {'name': 'pv1_power_low', 'scale': 1, 'unit': '', 'pair': 5, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 2
        7: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V'},
        8: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A'},
        9: {'name': 'pv2_power_high', 'scale': 1, 'unit': '', 'pair': 10},
        10: {'name': 'pv2_power_low', 'scale': 1, 'unit': '', 'pair': 9, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV String 3
        11: {'name': 'pv3_voltage', 'scale': 0.1, 'unit': 'V'},
        12: {'name': 'pv3_current', 'scale': 0.1, 'unit': 'A'},
        13: {'name': 'pv3_power_high', 'scale': 1, 'unit': '', 'pair': 14},
        14: {'name': 'pv3_power_low', 'scale': 1, 'unit': '', 'pair': 13, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Output Power
        35: {'name': 'output_power_high', 'scale': 1, 'unit': '', 'pair': 36},
        36: {'name': 'output_power_low', 'scale': 1, 'unit': '', 'pair': 35, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Grid Frequency
        37: {'name': 'grid_frequency', 'scale': 0.01, 'unit': 'Hz'},
        
        # Phase R (L1)
        38: {'name': 'grid_voltage_r', 'scale': 0.1, 'unit': 'V', 'desc': 'Phase R voltage'},
        39: {'name': 'grid_current_r', 'scale': 0.1, 'unit': 'A', 'desc': 'Phase R current'},
        40: {'name': 'grid_power_r_high', 'scale': 1, 'unit': '', 'pair': 41},
        41: {'name': 'grid_power_r_low', 'scale': 1, 'unit': '', 'pair': 40, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Phase S (L2)
        42: {'name': 'grid_voltage_s', 'scale': 0.1, 'unit': 'V', 'desc': 'Phase S voltage'},
        43: {'name': 'grid_current_s', 'scale': 0.1, 'unit': 'A', 'desc': 'Phase S current'},
        44: {'name': 'grid_power_s_high', 'scale': 1, 'unit': '', 'pair': 45},
        45: {'name': 'grid_power_s_low', 'scale': 1, 'unit': '', 'pair': 44, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Phase T (L3)
        46: {'name': 'grid_voltage_t', 'scale': 0.1, 'unit': 'V', 'desc': 'Phase T voltage'},
        47: {'name': 'grid_current_t', 'scale': 0.1, 'unit': 'A', 'desc': 'Phase T current'},
        48: {'name': 'grid_power_t_high', 'scale': 1, 'unit': '', 'pair': 49},
        49: {'name': 'grid_power_t_low', 'scale': 1, 'unit': '', 'pair': 48, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Line voltages
        50: {'name': 'grid_voltage_rs', 'scale': 0.1, 'unit': 'V', 'desc': 'Line voltage R-S'},
        51: {'name': 'grid_voltage_st', 'scale': 0.1, 'unit': 'V', 'desc': 'Line voltage S-T'},
        52: {'name': 'grid_voltage_tr', 'scale': 0.1, 'unit': 'V', 'desc': 'Line voltage T-R'},
        
        # Energy
        53: {'name': 'energy_today_high', 'scale': 1, 'unit': '', 'pair': 54},
        54: {'name': 'energy_today_low', 'scale': 1, 'unit': '', 'pair': 53, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        55: {'name': 'energy_total_high', 'scale': 1, 'unit': '', 'pair': 56},
        56: {'name': 'energy_total_low', 'scale': 1, 'unit': '', 'pair': 55, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Temperatures
        93: {'name': 'inverter_temp', 'scale': 0.1, 'unit': '°C'},
        94: {'name': 'ipm_temp', 'scale': 0.1, 'unit': '°C'},
        95: {'name': 'boost_temp', 'scale': 0.1, 'unit': '°C'},
        
        # Status
        100: {'name': 'power_factor', 'scale': 1, 'unit': ''},
        104: {'name': 'derating_mode', 'scale': 1, 'unit': ''},
        105: {'name': 'fault_code', 'scale': 1, 'unit': ''},
        112: {'name': 'warning_code', 'scale': 1, 'unit': ''},
    },
    'holding_registers': {
        0: {'name': 'on_off', 'scale': 1, 'unit': '', 'access': 'RW'},
        3: {'name': 'active_power_rate', 'scale': 1, 'unit': '%', 'access': 'RW'},
        30: {'name': 'modbus_address', 'scale': 1, 'unit': '', 'access': 'RW'},
    }
}

# MOD TL3-XH Series (Three-phase Hybrid with battery, 6-15kW)
MOD_6000_15000TL3_XH = {
    'name': 'MOD-6000-15000TL3-XH',
    'description': 'Modular three-phase hybrid inverter with battery (6-15kW)',
    'notes': 'Uses 0-124, 3000-3124, 3250-3374 register ranges. Includes battery.',
    'input_registers': {
        # System Status (from 3000 range for MOD)
        3000: {'name': 'inverter_status', 'scale': 1, 'unit': '', 'desc': '0=Waiting, 1=Normal, 3=Fault'},
        
        # PV Total Power
        3001: {'name': 'pv_total_power_high', 'scale': 1, 'unit': '', 'pair': 3002},
        3002: {'name': 'pv_total_power_low', 'scale': 1, 'unit': '', 'pair': 3001, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # PV Strings (same as MIN series)
        3003: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V'},
        3004: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A'},
        3005: {'name': 'pv1_power_high', 'scale': 1, 'unit': '', 'pair': 3006},
        3006: {'name': 'pv1_power_low', 'scale': 1, 'unit': '', 'pair': 3005, 'combined_scale': 0.1, 'combined_unit': 'W'},
        3007: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V'},
        3008: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A'},
        3009: {'name': 'pv2_power_high', 'scale': 1, 'unit': '', 'pair': 3010},
        3010: {'name': 'pv2_power_low', 'scale': 1, 'unit': '', 'pair': 3009, 'combined_scale': 0.1, 'combined_unit': 'W'},
        3011: {'name': 'pv3_voltage', 'scale': 0.1, 'unit': 'V'},
        3012: {'name': 'pv3_current', 'scale': 0.1, 'unit': 'A'},
        3013: {'name': 'pv3_power_high', 'scale': 1, 'unit': '', 'pair': 3014},
        3014: {'name': 'pv3_power_low', 'scale': 1, 'unit': '', 'pair': 3013, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # AC Output - Three Phase
        3025: {'name': 'ac_frequency', 'scale': 0.01, 'unit': 'Hz'},
        
        # Phase R
        3026: {'name': 'ac_voltage_r', 'scale': 0.1, 'unit': 'V'},
        3027: {'name': 'ac_current_r', 'scale': 0.1, 'unit': 'A'},
        3028: {'name': 'ac_power_r_high', 'scale': 1, 'unit': '', 'pair': 3029},
        3029: {'name': 'ac_power_r_low', 'scale': 1, 'unit': '', 'pair': 3028, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Phase S
        3030: {'name': 'ac_voltage_s', 'scale': 0.1, 'unit': 'V'},
        3031: {'name': 'ac_current_s', 'scale': 0.1, 'unit': 'A'},
        3032: {'name': 'ac_power_s_high', 'scale': 1, 'unit': '', 'pair': 3033},
        3033: {'name': 'ac_power_s_low', 'scale': 1, 'unit': '', 'pair': 3032, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Phase T
        3034: {'name': 'ac_voltage_t', 'scale': 0.1, 'unit': 'V'},
        3035: {'name': 'ac_current_t', 'scale': 0.1, 'unit': 'A'},
        3036: {'name': 'ac_power_t_high', 'scale': 1, 'unit': '', 'pair': 3037},
        3037: {'name': 'ac_power_t_low', 'scale': 1, 'unit': '', 'pair': 3036, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        
        # Line voltages
        3038: {'name': 'grid_voltage_rs', 'scale': 0.1, 'unit': 'V'},
        3039: {'name': 'grid_voltage_st', 'scale': 0.1, 'unit': 'V'},
        3040: {'name': 'grid_voltage_tr', 'scale': 0.1, 'unit': 'V'},
        
        # Power Flow
        3041: {'name': 'power_to_user_high', 'scale': 1, 'unit': '', 'pair': 3042},
        3042: {'name': 'power_to_user_low', 'scale': 1, 'unit': '', 'pair': 3041, 'combined_scale': 0.1, 'combined_unit': 'W'},
        3043: {'name': 'power_to_grid_high', 'scale': 1, 'unit': '', 'pair': 3044},
        3044: {'name': 'power_to_grid_low', 'scale': 1, 'unit': '', 'pair': 3043, 'combined_scale': 0.1, 'combined_unit': 'W', 'signed': True},
        3045: {'name': 'power_to_load_high', 'scale': 1, 'unit': '', 'pair': 3046},
        3046: {'name': 'power_to_load_low', 'scale': 1, 'unit': '', 'pair': 3045, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Energy
        3049: {'name': 'energy_today_high', 'scale': 1, 'unit': '', 'pair': 3050},
        3050: {'name': 'energy_today_low', 'scale': 1, 'unit': '', 'pair': 3049, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3051: {'name': 'energy_total_high', 'scale': 1, 'unit': '', 'pair': 3052},
        3052: {'name': 'energy_total_low', 'scale': 1, 'unit': '', 'pair': 3051, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Energy Breakdown
        3067: {'name': 'energy_to_user_today_high', 'scale': 1, 'unit': '', 'pair': 3068},
        3068: {'name': 'energy_to_user_today_low', 'scale': 1, 'unit': '', 'pair': 3067, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3071: {'name': 'energy_to_grid_today_high', 'scale': 1, 'unit': '', 'pair': 3072},
        3072: {'name': 'energy_to_grid_today_low', 'scale': 1, 'unit': '', 'pair': 3071, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3075: {'name': 'load_energy_today_high', 'scale': 1, 'unit': '', 'pair': 3076},
        3076: {'name': 'load_energy_today_low', 'scale': 1, 'unit': '', 'pair': 3075, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Battery - Discharge/Charge Energy (today)
        3125: {'name': 'battery_discharge_today_high', 'scale': 1, 'unit': '', 'pair': 3126},
        3126: {'name': 'battery_discharge_today_low', 'scale': 1, 'unit': '', 'pair': 3125, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3127: {'name': 'battery_discharge_total_high', 'scale': 1, 'unit': '', 'pair': 3128},
        3128: {'name': 'battery_discharge_total_low', 'scale': 1, 'unit': '', 'pair': 3127, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3129: {'name': 'battery_charge_today_high', 'scale': 1, 'unit': '', 'pair': 3130},
        3130: {'name': 'battery_charge_today_low', 'scale': 1, 'unit': '', 'pair': 3129, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3131: {'name': 'battery_charge_total_high', 'scale': 1, 'unit': '', 'pair': 3132},
        3132: {'name': 'battery_charge_total_low', 'scale': 1, 'unit': '', 'pair': 3131, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        
        # Battery State
        3144: {'name': 'priority_mode', 'scale': 1, 'unit': '', 'desc': '0=Load, 1=Battery, 2=Grid'},
        3165: {'name': 'battery_derating_mode', 'scale': 1, 'unit': ''},
        3169: {'name': 'battery_voltage', 'scale': 0.01, 'unit': 'V'},
        3170: {'name': 'battery_current', 'scale': 0.1, 'unit': 'A'},
        3171: {'name': 'battery_soc', 'scale': 1, 'unit': '%'},
        3176: {'name': 'battery_temp', 'scale': 0.1, 'unit': '°C'},
        3178: {'name': 'battery_discharge_power_high', 'scale': 1, 'unit': '', 'pair': 3179},
        3179: {'name': 'battery_discharge_power_low', 'scale': 1, 'unit': '', 'pair': 3178, 'combined_scale': 0.1, 'combined_unit': 'W'},
        3180: {'name': 'battery_charge_power_high', 'scale': 1, 'unit': '', 'pair': 3181},
        3181: {'name': 'battery_charge_power_low', 'scale': 1, 'unit': '', 'pair': 3180, 'combined_scale': 0.1, 'combined_unit': 'W'},
        
        # Temperatures
        3093: {'name': 'inverter_temp', 'scale': 0.1, 'unit': '°C'},
        3094: {'name': 'ipm_temp', 'scale': 0.1, 'unit': '°C'},
        3095: {'name': 'boost_temp', 'scale': 0.1, 'unit': '°C'},
        
        # Status
        3086: {'name': 'derating_mode', 'scale': 1, 'unit': ''},
        3105: {'name': 'fault_code', 'scale': 1, 'unit': ''},
        3106: {'name': 'warning_code', 'scale': 1, 'unit': ''},
    },
    'holding_registers': {
        0: {'name': 'on_off', 'scale': 1, 'unit': '', 'access': 'RW'},
        3: {'name': 'active_power_rate', 'scale': 1, 'unit': '%', 'access': 'RW'},
        30: {'name': 'modbus_address', 'scale': 1, 'unit': '', 'access': 'RW'},
    }
}

# MIN Series Base Range (0-124) - Legacy/Alternative addressing
# Some implementations access the same data at base 0 instead of 3000
MIN_SERIES_BASE_RANGE = {
    'name': 'MIN Series Base Range (0-124)',
    'description': 'Alternative register addressing starting at 0 instead of 3000',
    'notes': 'Contains same data as 3000 range. Use for devices that expect base 0 addressing.',
    'input_registers': {
        0: {'name': 'inverter_status', 'scale': 1, 'unit': '', 'desc': '0=Waiting, 1=Normal, 3=Fault'},
        1: {'name': 'input_power_high', 'scale': 1, 'unit': '', 'pair': 2},
        2: {'name': 'input_power_low', 'scale': 1, 'unit': '', 'pair': 1, 'combined_scale': 0.1, 'combined_unit': 'W'},
        3: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V'},
        4: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A'},
        5: {'name': 'pv1_power_high', 'scale': 1, 'unit': '', 'pair': 6},
        6: {'name': 'pv1_power_low', 'scale': 1, 'unit': '', 'pair': 5, 'combined_scale': 0.1, 'combined_unit': 'W'},
        7: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V'},
        8: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A'},
        9: {'name': 'pv2_power_high', 'scale': 1, 'unit': '', 'pair': 10},
        10: {'name': 'pv2_power_low', 'scale': 1, 'unit': '', 'pair': 9, 'combined_scale': 0.1, 'combined_unit': 'W'},
        11: {'name': 'pv3_voltage', 'scale': 0.1, 'unit': 'V'},
        12: {'name': 'pv3_current', 'scale': 0.1, 'unit': 'A'},
        13: {'name': 'pv3_power_high', 'scale': 1, 'unit': '', 'pair': 14},
        14: {'name': 'pv3_power_low', 'scale': 1, 'unit': '', 'pair': 13, 'combined_scale': 0.1, 'combined_unit': 'W'},
        35: {'name': 'output_power_high', 'scale': 1, 'unit': '', 'pair': 36},
        36: {'name': 'output_power_low', 'scale': 1, 'unit': '', 'pair': 35, 'combined_scale': 0.1, 'combined_unit': 'W'},
        37: {'name': 'grid_frequency', 'scale': 0.01, 'unit': 'Hz'},
        38: {'name': 'grid_voltage', 'scale': 0.1, 'unit': 'V'},
        39: {'name': 'grid_current', 'scale': 0.1, 'unit': 'A'},
        40: {'name': 'grid_power_high', 'scale': 1, 'unit': '', 'pair': 41},
        41: {'name': 'grid_power_low', 'scale': 1, 'unit': '', 'pair': 40, 'combined_scale': 0.1, 'combined_unit': 'VA'},
        53: {'name': 'energy_today_high', 'scale': 1, 'unit': '', 'pair': 54},
        54: {'name': 'energy_today_low', 'scale': 1, 'unit': '', 'pair': 53, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        55: {'name': 'energy_total_high', 'scale': 1, 'unit': '', 'pair': 56},
        56: {'name': 'energy_total_low', 'scale': 1, 'unit': '', 'pair': 55, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        57: {'name': 'time_total_high', 'scale': 1, 'unit': '', 'pair': 58},
        58: {'name': 'time_total_low', 'scale': 1, 'unit': '', 'pair': 57, 'combined_scale': 0.5, 'combined_unit': 's'},
        93: {'name': 'inverter_temp', 'scale': 0.1, 'unit': '°C'},
        94: {'name': 'ipm_temp', 'scale': 0.1, 'unit': '°C'},
        95: {'name': 'boost_temp', 'scale': 0.1, 'unit': '°C'},
        98: {'name': 'p_bus_voltage', 'scale': 0.1, 'unit': 'V'},
        99: {'name': 'n_bus_voltage', 'scale': 0.1, 'unit': 'V'},
        100: {'name': 'power_factor', 'scale': 1, 'unit': '', 'desc': '0-10000=underexcited, 10001-20000=overexcited'},
        104: {'name': 'derating_mode', 'scale': 1, 'unit': ''},
        105: {'name': 'fault_code', 'scale': 1, 'unit': ''},
        107: {'name': 'fault_subcode', 'scale': 1, 'unit': ''},
        110: {'name': 'warning_high', 'scale': 1, 'unit': ''},
        111: {'name': 'warning_subcode', 'scale': 1, 'unit': ''},
        112: {'name': 'warning_code', 'scale': 1, 'unit': ''},
    },
    'holding_registers': {
        0: {'name': 'on_off', 'scale': 1, 'unit': '', 'access': 'RW'},
        3: {'name': 'active_power_rate', 'scale': 1, 'unit': '%', 'access': 'RW'},
        15: {'name': 'lcd_language', 'scale': 1, 'unit': '', 'access': 'RW'},
        22: {'name': 'baud_rate', 'scale': 1, 'unit': '', 'access': 'RW'},
        30: {'name': 'modbus_address', 'scale': 1, 'unit': '', 'access': 'RW'},
        45: {'name': 'sys_year', 'scale': 1, 'unit': '', 'access': 'RW'},
        46: {'name': 'sys_month', 'scale': 1, 'unit': '', 'access': 'RW'},
        47: {'name': 'sys_day', 'scale': 1, 'unit': '', 'access': 'RW'},
        48: {'name': 'sys_hour', 'scale': 1, 'unit': '', 'access': 'RW'},
        49: {'name': 'sys_min', 'scale': 1, 'unit': '', 'access': 'RW'},
        50: {'name': 'sys_sec', 'scale': 1, 'unit': '', 'access': 'RW'},
    }
}

# ============================================================================
# NEW PROFILES - Added to support all Protocol V1.39 models
# ============================================================================

# TL-XH Series (Hybrid MIN with battery) - Uses same base as MIN_7000_10000TL_X
TL_XH_3000_10000 = {
    'name': 'TL-XH-3000-10000',
    'description': 'Hybrid single-phase inverter with battery (3-10kW)',
    'notes': 'Uses 3000-3124 register range. Extends MIN series with battery support.',
    'input_registers': {
        **MIN_7000_10000TL_X['input_registers'],  # Inherit all MIN registers
        # Battery-specific registers (if different from MOD series)
        3165: {'name': 'battery_derating_mode', 'scale': 1, 'unit': ''},
        3169: {'name': 'battery_voltage', 'scale': 0.01, 'unit': 'V'},
        3170: {'name': 'battery_current', 'scale': 0.1, 'unit': 'A'},
        3171: {'name': 'battery_soc', 'scale': 1, 'unit': '%'},
    },
    'holding_registers': MIN_7000_10000TL_X['holding_registers'],
}

# TL-XH US Series (US version with extended range)
TL_XH_US_3000_10000 = {
    'name': 'TL-XH-US-3000-10000',
    'description': 'US hybrid single-phase inverter with battery (3-10kW)',
    'notes': 'Uses 3000-3249 register range. US-specific features and battery support.',
    'input_registers': {
        **TL_XH_3000_10000['input_registers'],  # Inherit TL-XH registers
        # US-specific extended registers in 3125-3249 range
        3125: {'name': 'battery_discharge_today_high', 'scale': 1, 'unit': '', 'pair': 3126},
        3126: {'name': 'battery_discharge_today_low', 'scale': 1, 'unit': '', 'pair': 3125, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        3129: {'name': 'battery_charge_today_high', 'scale': 1, 'unit': '', 'pair': 3130},
        3130: {'name': 'battery_charge_today_low', 'scale': 1, 'unit': '', 'pair': 3129, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
    },
    'holding_registers': TL_XH_3000_10000['holding_registers'],
}

# MAC Series (Three-phase compact) - Similar to MID
MAC_20000_40000TL3_X = {
    'name': 'MAC-20000-40000TL3-X',
    'description': 'Compact three-phase commercial inverter (20-40kW)',
    'notes': 'Uses 0-124, 125-249 register range. Similar to MID series.',
    'input_registers': MID_15000_25000TL3_X['input_registers'],  # Shares register layout with MID
    'holding_registers': MID_15000_25000TL3_X['holding_registers'],
}

# MAX 1500V Series (High-voltage commercial)
MAX_1500V_SERIES = {
    'name': 'MAX-1500V',
    'description': 'High-voltage commercial three-phase inverter (up to 150kW)',
    'notes': 'Uses 0-124, 125-249, 875-999 register ranges.',
    'input_registers': {
        **MAX_50000_125000TL3_X['input_registers'],  # Inherit MAX registers
        # Extended PV strings in 875-999 range (PV9-PV16 for large arrays)
        875: {'name': 'pv9_voltage', 'scale': 0.1, 'unit': 'V'},
        876: {'name': 'pv9_current', 'scale': 0.1, 'unit': 'A'},
        877: {'name': 'pv9_power_high', 'scale': 1, 'unit': '', 'pair': 878},
        878: {'name': 'pv9_power_low', 'scale': 1, 'unit': '', 'pair': 877, 'combined_scale': 0.1, 'combined_unit': 'W'},
    },
    'holding_registers': MAX_50000_125000TL3_X['holding_registers'],
}

# MAX-X LV Series (Low-voltage commercial)
MAX_X_LV_SERIES = {
    'name': 'MAX-X-LV',
    'description': 'Low-voltage commercial three-phase inverter (up to 125kW)',
    'notes': 'Uses 0-124, 125-249, 875-999 register ranges.',
    'input_registers': MAX_1500V_SERIES['input_registers'],  # Same layout as MAX 1500V
    'holding_registers': MAX_1500V_SERIES['holding_registers'],
}

# MIX Series (Legacy storage) - Similar to SPH
MIX_SERIES = {
    'name': 'MIX Series',
    'description': 'Legacy storage inverter (merged into SPH per protocol v1.35)',
    'notes': 'Uses 0-124, 1000-1124 register range. Battery storage system.',
    'input_registers': SPH_3000_10000['input_registers'],  # Shares register layout with SPH
    'holding_registers': SPH_3000_10000['holding_registers'],
}

# SPA Series (AC-coupled storage)
SPA_SERIES = {
    'name': 'SPA Series',
    'description': 'AC-coupled storage inverter',
    'notes': 'Uses 0-124, 1000-1124 register range. AC-coupled battery system.',
    'input_registers': {
        # System Status
        1000: {'name': 'system_work_mode', 'scale': 1, 'unit': '', 'desc': 'Work mode'},
        
        # Battery (same as SPH)
        1013: {'name': 'battery_voltage', 'scale': 0.1, 'unit': 'V'},
        1014: {'name': 'battery_soc', 'scale': 1, 'unit': '%'},
        1040: {'name': 'battery_temp', 'scale': 0.1, 'unit': '°C'},
        
        # Power Flow
        1015: {'name': 'power_to_user_high', 'scale': 1, 'unit': '', 'pair': 1016},
        1016: {'name': 'power_to_user_low', 'scale': 1, 'unit': '', 'pair': 1015, 'combined_scale': 0.1, 'combined_unit': 'W'},
        1029: {'name': 'power_to_grid_high', 'scale': 1, 'unit': '', 'pair': 1030},
        1030: {'name': 'power_to_grid_low', 'scale': 1, 'unit': '', 'pair': 1029, 'combined_scale': 0.1, 'combined_unit': 'W', 'signed': True},
        
        # Energy
        1044: {'name': 'energy_to_user_today_high', 'scale': 1, 'unit': '', 'pair': 1045},
        1045: {'name': 'energy_to_user_today_low', 'scale': 1, 'unit': '', 'pair': 1044, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
        1048: {'name': 'energy_to_grid_today_high', 'scale': 1, 'unit': '', 'pair': 1049},
        1049: {'name': 'energy_to_grid_today_low', 'scale': 1, 'unit': '', 'pair': 1048, 'combined_scale': 0.1, 'combined_unit': 'kWh'},
    },
    'holding_registers': {
        0: {'name': 'on_off', 'scale': 1, 'unit': '', 'access': 'RW'},
        1044: {'name': 'priority', 'scale': 1, 'unit': '', 'access': 'RW', 'desc': '0=Load, 1=Battery, 2=Grid'},
    }
}

# WIT TL3 Series (Business storage power)
WIT_TL3_SERIES = {
    'name': 'WIT-TL3',
    'description': 'Business storage power three-phase inverter',
    'notes': 'Uses 0-124, 125-249, 875-999, 8000-8124 register ranges.',
    'input_registers': {
        # Inherits three-phase base from MAX series
        **MAX_50000_125000TL3_X['input_registers'],
        
        # Battery from MOD series (3000 range mapped to 8000 range for WIT)
        8034: {'name': 'battery_voltage', 'scale': 0.1, 'unit': 'V'},
        8035: {'name': 'battery_current', 'scale': 0.1, 'unit': 'A'},
        8093: {'name': 'battery_soc', 'scale': 1, 'unit': '%'},
        8094: {'name': 'battery_soh', 'scale': 1, 'unit': '%'},
        
        # Extended PV in 875-999 range
        875: {'name': 'pv9_voltage', 'scale': 0.1, 'unit': 'V'},
        876: {'name': 'pv9_current', 'scale': 0.1, 'unit': 'A'},
        877: {'name': 'pv9_power_high', 'scale': 1, 'unit': '', 'pair': 878},
        878: {'name': 'pv9_power_low', 'scale': 1, 'unit': '', 'pair': 877, 'combined_scale': 0.1, 'combined_unit': 'W'},
        879: {'name': 'pv10_voltage', 'scale': 0.1, 'unit': 'V'},
        880: {'name': 'pv10_current', 'scale': 0.1, 'unit': 'A'},
        881: {'name': 'pv10_power_high', 'scale': 1, 'unit': '', 'pair': 882},
        882: {'name': 'pv10_power_low', 'scale': 1, 'unit': '', 'pair': 881, 'combined_scale': 0.1, 'combined_unit': 'W'},
    },
    'holding_registers': {
        0: {'name': 'on_off', 'scale': 1, 'unit': '', 'access': 'RW'},
        3: {'name': 'active_power_rate', 'scale': 1, 'unit': '%', 'access': 'RW'},
        30: {'name': 'modbus_address', 'scale': 1, 'unit': '', 'access': 'RW'},
        871: {'name': 'grid_phase_sequence', 'scale': 1, 'unit': '', 'access': 'RW', 'desc': '0=Positive, 1=Reverse'},
        874: {'name': 'parallel_enable', 'scale': 1, 'unit': '', 'access': 'RW', 'desc': '0=Disable, 1=Enable'},
    }
}

# ============================================================================
# Main register map dictionary - ALL 14 PROFILES
# ============================================================================

REGISTER_MAPS = {
    # MIN Series - Single Phase String
    'MIN_3000_6000TL_X': MIN_3000_6000TL_X,
    'MIN_7000_10000TL_X': MIN_7000_10000TL_X,
    'MIN_SERIES_BASE_RANGE': MIN_SERIES_BASE_RANGE,  # Legacy/alternative addressing
    
    # TL-XH Series - Single Phase Hybrid
    'TL_XH_3000_10000': TL_XH_3000_10000,
    'TL_XH_US_3000_10000': TL_XH_US_3000_10000,
    
    # MID Series - Three Phase String
    'MID_15000_25000TL3_X': MID_15000_25000TL3_X,
    
    # MAC Series - Three Phase Compact
    'MAC_20000_40000TL3_X': MAC_20000_40000TL3_X,
    
    # MAX Series - Commercial Three Phase
    'MAX_50000_125000TL3_X': MAX_50000_125000TL3_X,
    'MAX_1500V_SERIES': MAX_1500V_SERIES,
    'MAX_X_LV_SERIES': MAX_X_LV_SERIES,
    
    # SPH Series - Hybrid Storage Single Phase
    'SPH_3000_10000': SPH_3000_10000,
    
    # MIX Series - Legacy Storage
    'MIX_SERIES': MIX_SERIES,
    
    # SPA Series - AC Coupled Storage
    'SPA_SERIES': SPA_SERIES,
    
    # MOD Series - Modular Three Phase Hybrid
    'MOD_6000_15000TL3_XH': MOD_6000_15000TL3_XH,
    
    # WIT Series - Business Storage Power
    'WIT_TL3_SERIES': WIT_TL3_SERIES,
}

# Status code mappings
STATUS_CODES = {
    0: {'name': 'Waiting', 'desc': 'Waiting for sufficient PV power or grid conditions'},
    1: {'name': 'Normal', 'desc': 'Operating normally'},
    3: {'name': 'Fault', 'desc': 'Fault condition detected'},
}

# Helper functions
def combine_registers(high, low):
    """Combine two 16-bit registers into 32-bit value"""
    return (high << 16) | low

def scale_value(raw_value, scale):
    """Apply scaling factor to raw register value"""
    return raw_value * scale

def get_register_info(register_map_name, register_type, address):
    """Get information about a specific register"""
    if register_map_name not in REGISTER_MAPS:
        return None
    
    register_map = REGISTER_MAPS[register_map_name]
    registers = register_map.get(f'{register_type}_registers', {})
    
    return registers.get(address, None)

def get_status_name(status_code):
    """Get human-readable status name"""
    return STATUS_CODES.get(status_code, {'name': f'Unknown ({status_code})', 'desc': 'Unknown status code'})

def list_available_maps():
    """List all available register maps"""
    for name, config in REGISTER_MAPS.items():
        print(f"{name}: {config['name']}")
        print(f"  Description: {config['description']}")
        if 'notes' in config:
            print(f"  Notes: {config['notes']}")
        print()

if __name__ == "__main__":
    print("Growatt Register Maps (Protocol V1.39)")
    print("=" * 50)
    list_available_maps()
    
    # Example: Combining 32-bit power register
    print("\nExample: Reading PV1 Power")
    print("-" * 50)
    pv1_high = 0  # Example HIGH word
    pv1_low = 12450  # Example LOW word (1245.0W)
    combined = combine_registers(pv1_high, pv1_low)
    scaled = scale_value(combined, 0.1)
    print(f"HIGH: {pv1_high}, LOW: {pv1_low}")
    print(f"Combined: {combined}, Scaled: {scaled}W")