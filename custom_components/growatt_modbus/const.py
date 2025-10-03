#!/usr/bin/env python3
"""
Growatt Inverter Register Definitions and Integration Constants
Modbus register mappings for Growatt MIN series inverters
Based on official Growatt Protocol V1.39 (2024.04.16)

REQUIREMENTS:
- Python 3.7+

Usage:
    from const import REGISTER_MAPS
    registers = REGISTER_MAPS['MIN_10000_TL_X_OFFICIAL']
"""

# Home Assistant Integration Constants
DOMAIN = "growatt_modbus"

# Configuration Constants
CONF_SLAVE_ID = "slave_id"
CONF_CONNECTION_TYPE = "connection_type"
CONF_DEVICE_PATH = "device_path"
CONF_BAUDRATE = "baudrate"
CONF_REGISTER_MAP = "register_map"

# Default Values
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1
DEFAULT_BAUDRATE = 9600

# MIN-10000-TL-X Official Mapping (Protocol V1.39)
# Based on official Growatt documentation
# Uses INPUT_REGISTERS_STORAGE range (3000-3124)
MIN_10000_TL_X_OFFICIAL = {
    'name': 'MIN-10000-TL-X Official (Protocol V1.39)',
    'description': 'Official register mapping from Growatt Protocol V1.39 documentation',
    'notes': 'Power registers are 32-bit pairs (HIGH/LOW). Grid frequency uses raw register 37.',
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
        
        # Power Flow (32-bit pairs)
        3041: {'name': 'power_to_user_high', 'scale': 1, 'unit': '', 'desc': 'Forward power HIGH', 'pair': 3042},
        3042: {'name': 'power_to_user_low', 'scale': 1, 'unit': '', 'desc': 'Forward power LOW', 'pair': 3041, 'combined_scale': 0.1, 'combined_unit': 'W'},
        3043: {'name': 'power_to_grid_high', 'scale': 1, 'unit': '', 'desc': 'Export power HIGH', 'pair': 3044},
        3044: {'name': 'power_to_grid_low', 'scale': 1, 'unit': '', 'desc': 'Export power LOW', 'pair': 3043, 'combined_scale': 0.1, 'combined_unit': 'W'},
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

# MIN Series Base Range (0-124) - Alternative addressing
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

# Main register map dictionary
REGISTER_MAPS = {
    'MIN_10000_TL_X_OFFICIAL': MIN_10000_TL_X_OFFICIAL,
    'MIN_SERIES_BASE_RANGE': MIN_SERIES_BASE_RANGE,
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
    print("Growatt Register Maps (Official V1.39)")
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