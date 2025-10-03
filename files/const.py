#!/usr/bin/env python3
"""
Growatt Inverter Register Definitions
Modbus register mappings for different Growatt models

REQUIREMENTS:
- Python 3.7+

Usage:
    from const import REGISTER_MAPS
    registers = REGISTER_MAPS['MIN_10000_VARIANT_A']
"""

# Default MIN series mapping (from official documentation)
MIN_SERIES_STANDARD = {
    'name': 'MIN Series Standard (TL-X)',
    'description': 'Standard register mapping from Growatt documentation',
    'input_registers': {
        3000: {'name': 'inverter_status', 'scale': 1, 'unit': '', 'desc': 'Operating status'},
        3001: {'name': 'pv_total_power', 'scale': 0.1, 'unit': 'W', 'desc': 'Combined PV power'},
        3003: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'String 1 voltage'},
        3004: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A', 'desc': 'String 1 current'},
        3005: {'name': 'pv1_power', 'scale': 0.1, 'unit': 'W', 'desc': 'String 1 power'},
        3006: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'String 2 voltage'},
        3007: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A', 'desc': 'String 2 current'},
        3008: {'name': 'pv2_power', 'scale': 0.1, 'unit': 'W', 'desc': 'String 2 power'},
        3011: {'name': 'ac_power', 'scale': 0.1, 'unit': 'W', 'desc': 'AC output power'},
        3012: {'name': 'ac_frequency', 'scale': 0.01, 'unit': 'Hz', 'desc': 'Grid frequency'},
        3013: {'name': 'ac_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'Grid voltage'},
        3014: {'name': 'ac_current', 'scale': 0.1, 'unit': 'A', 'desc': 'AC output current'},
        3017: {'name': 'temperature', 'scale': 0.1, 'unit': '°C', 'desc': 'Internal temperature'},
        3026: {'name': 'energy_today', 'scale': 0.1, 'unit': 'kWh', 'desc': 'Today energy'},
        3028: {'name': 'energy_total_high', 'scale': 1, 'unit': '', 'desc': 'Total energy (high word)'},
        3029: {'name': 'energy_total_low', 'scale': 1, 'unit': '', 'desc': 'Total energy (low word)'},
        
        # Smart Meter registers (when connected)
        3046: {'name': 'grid_power', 'scale': 0.1, 'unit': 'W', 'desc': 'Grid power (+export/-import)'},
        3047: {'name': 'grid_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'Grid voltage from meter'},
        3048: {'name': 'grid_current', 'scale': 0.1, 'unit': 'A', 'desc': 'Grid current from meter', 'signed': True},
        3049: {'name': 'grid_frequency', 'scale': 0.01, 'unit': 'Hz', 'desc': 'Grid frequency from meter'},
        3050: {'name': 'load_power', 'scale': 0.1, 'unit': 'W', 'desc': 'House consumption'},
    },
    'holding_registers': {
        0: {'name': 'safety_func_en', 'scale': 1, 'unit': '', 'desc': 'Safety function enable'},
        3: {'name': 'firmware_version', 'scale': 1, 'unit': '', 'desc': 'Firmware version'},
        9: {'name': 'serial_number_1', 'scale': 1, 'unit': '', 'desc': 'Serial number part 1'},
        10: {'name': 'serial_number_2', 'scale': 1, 'unit': '', 'desc': 'Serial number part 2'},
        11: {'name': 'serial_number_3', 'scale': 1, 'unit': '', 'desc': 'Serial number part 3'},
        12: {'name': 'serial_number_4', 'scale': 1, 'unit': '', 'desc': 'Serial number part 4'},
        13: {'name': 'serial_number_5', 'scale': 1, 'unit': '', 'desc': 'Serial number part 5'},
        100: {'name': 'modbus_address', 'scale': 1, 'unit': '', 'desc': 'Modbus slave address'},
    }
}

# MIN-10000 Variant A (discovered from real hardware)
# This variant has PV2 power register before voltage/current
MIN_10000_VARIANT_A = {
    'name': 'MIN-10000 Variant A',
    'description': 'Real-world mapping discovered from MIN-10000 hardware (Serial: AM1.0ZABA)',
    'notes': 'PV2 power register comes before voltage/current registers',
    'input_registers': {
        3000: {'name': 'inverter_status', 'scale': 1, 'unit': '', 'desc': 'Operating status'},
        3001: {'name': 'pv_total_power', 'scale': 0.1, 'unit': 'W', 'desc': 'Combined PV power'},
        3002: {'name': 'unknown_3002', 'scale': 0.1, 'unit': '?', 'desc': 'Unknown register'},
        3003: {'name': 'pv1_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'String 1 voltage'},
        3004: {'name': 'pv1_current', 'scale': 0.1, 'unit': 'A', 'desc': 'String 1 current'},
        3005: {'name': 'pv1_power', 'scale': 0.1, 'unit': 'W', 'desc': 'String 1 power'},
        3006: {'name': 'pv2_power', 'scale': 0.1, 'unit': 'W', 'desc': 'String 2 power (non-standard location!)'},
        3007: {'name': 'pv2_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'String 2 voltage'},
        3008: {'name': 'pv2_current', 'scale': 0.1, 'unit': 'A', 'desc': 'String 2 current'},
        3009: {'name': 'pv2_power_alt', 'scale': 0.1, 'unit': 'W', 'desc': 'Alternative PV2 power register'},
        3010: {'name': 'unknown_3010', 'scale': 0.1, 'unit': '?', 'desc': 'Unknown register'},
        3011: {'name': 'ac_power', 'scale': 0.1, 'unit': 'W', 'desc': 'AC output power'},
        3012: {'name': 'ac_frequency', 'scale': 0.01, 'unit': 'Hz', 'desc': 'Grid frequency'},
        3013: {'name': 'ac_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'Grid voltage'},
        3014: {'name': 'ac_current', 'scale': 0.1, 'unit': 'A', 'desc': 'AC output current'},
        3017: {'name': 'temperature', 'scale': 0.1, 'unit': '°C', 'desc': 'Internal temperature'},
        3020: {'name': 'unknown_3020', 'scale': 0.1, 'unit': '?', 'desc': 'Unknown register (matches 3002)'},
        3024: {'name': 'unknown_3024', 'scale': 0.1, 'unit': '?', 'desc': 'Unknown register'},
        3025: {'name': 'unknown_3025', 'scale': 0.1, 'unit': '?', 'desc': 'Unknown register'},
        3026: {'name': 'energy_today', 'scale': 0.1, 'unit': 'kWh', 'desc': 'Today energy'},
        3028: {'name': 'energy_total_high', 'scale': 1, 'unit': '', 'desc': 'Total energy (high word)'},
        3029: {'name': 'energy_total_low', 'scale': 1, 'unit': '', 'desc': 'Total energy (low word)'},
        
        # Smart Meter registers (when connected)
        3046: {'name': 'grid_power', 'scale': 0.1, 'unit': 'W', 'desc': 'Grid power (+export/-import)', 'signed': True},
        3047: {'name': 'grid_voltage', 'scale': 0.1, 'unit': 'V', 'desc': 'Grid voltage from meter'},
        3048: {'name': 'grid_current', 'scale': 0.1, 'unit': 'A', 'desc': 'Grid current from meter', 'signed': True},
        3049: {'name': 'grid_frequency', 'scale': 0.01, 'unit': 'Hz', 'desc': 'Grid frequency from meter'},
        3050: {'name': 'load_power', 'scale': 0.1, 'unit': 'W', 'desc': 'House consumption'},
    },
    'holding_registers': {
        0: {'name': 'safety_func_en', 'scale': 1, 'unit': '', 'desc': 'Safety function enable'},
        3: {'name': 'firmware_version', 'scale': 1, 'unit': '', 'desc': 'Firmware version'},
        9: {'name': 'serial_number_1', 'scale': 1, 'unit': '', 'desc': 'Serial number part 1'},
        10: {'name': 'serial_number_2', 'scale': 1, 'unit': '', 'desc': 'Serial number part 2'},
        11: {'name': 'serial_number_3', 'scale': 1, 'unit': '', 'desc': 'Serial number part 3'},
        12: {'name': 'serial_number_4', 'scale': 1, 'unit': '', 'desc': 'Serial number part 4'},
        13: {'name': 'serial_number_5', 'scale': 1, 'unit': '', 'desc': 'Serial number part 5'},
        100: {'name': 'modbus_address', 'scale': 1, 'unit': '', 'desc': 'Modbus slave address'},
    }
}

# Main register map dictionary
REGISTER_MAPS = {
    'MIN_SERIES_STANDARD': MIN_SERIES_STANDARD,
    'MIN_10000_VARIANT_A': MIN_10000_VARIANT_A,
}

# Status code mappings
STATUS_CODES = {
    0: {'name': 'Standby', 'desc': 'Waiting for sufficient PV power'},
    1: {'name': 'Normal', 'desc': 'Operating normally'},
    2: {'name': 'Fault', 'desc': 'Fault condition detected'},
    3: {'name': 'Permanent Fault', 'desc': 'Serious fault requiring attention'},
    4: {'name': 'Check', 'desc': 'Self-check mode'},
    5: {'name': 'Waiting', 'desc': 'Waiting for grid conditions'},
}

# Helper functions
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
    print("Available Growatt Register Maps:")
    print("=" * 40)
    list_available_maps()