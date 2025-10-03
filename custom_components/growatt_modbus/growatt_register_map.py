"""
Growatt MIN-10000-TL-X Modbus Register Map
Based on Protocol Version V1.39 (2024.04.16)

Applicable Models: TL-X/TL-XH (MIN Type)
Function Code 03 (Holding): 0-124, 3000-3124
Function Code 04 (Input): 0-124, 3000-3124

Register addressing note: Some implementations use base 0 (data[0]=register 0)
while others use base 3000 (register 3000). Both contain the same data.
"""

# INPUT REGISTERS (Function Code 0x04) - READ ONLY
# Base Range 0-124
INPUT_REGISTERS_BASE = {
    # Status and Power
    0: {"name": "Inverter_Status", "scale": 1, "unit": "", "description": "0=Waiting, 1=Normal, 3=Fault"},
    1: {"name": "Input_Power_H", "scale": 0.1, "unit": "W", "description": "Total input power HIGH", "pair": 2},
    2: {"name": "Input_Power_L", "scale": 0.1, "unit": "W", "description": "Total input power LOW", "pair": 1},
    
    # PV String 1
    3: {"name": "PV1_Voltage", "scale": 0.1, "unit": "V", "description": "PV1 DC voltage"},
    4: {"name": "PV1_Current", "scale": 0.1, "unit": "A", "description": "PV1 DC current"},
    5: {"name": "PV1_Power_H", "scale": 0.1, "unit": "W", "description": "PV1 power HIGH", "pair": 6},
    6: {"name": "PV1_Power_L", "scale": 0.1, "unit": "W", "description": "PV1 power LOW", "pair": 5},
    
    # PV String 2
    7: {"name": "PV2_Voltage", "scale": 0.1, "unit": "V", "description": "PV2 DC voltage"},
    8: {"name": "PV2_Current", "scale": 0.1, "unit": "A", "description": "PV2 DC current"},
    9: {"name": "PV2_Power_H", "scale": 0.1, "unit": "W", "description": "PV2 power HIGH", "pair": 10},
    10: {"name": "PV2_Power_L", "scale": 0.1, "unit": "W", "description": "PV2 power LOW", "pair": 9},
    
    # AC Output Power
    35: {"name": "Output_Power_H", "scale": 0.1, "unit": "W", "description": "Total AC output power HIGH", "pair": 36},
    36: {"name": "Output_Power_L", "scale": 0.1, "unit": "W", "description": "Total AC output power LOW", "pair": 35},
    
    # Grid Parameters (Single Phase)
    37: {"name": "Grid_Frequency", "scale": 0.01, "unit": "Hz", "description": "Grid frequency"},
    38: {"name": "Grid_Voltage", "scale": 0.1, "unit": "V", "description": "Grid voltage (Phase 1 for single-phase)"},
    39: {"name": "Grid_Current", "scale": 0.1, "unit": "A", "description": "Grid output current"},
    40: {"name": "Grid_Power_H", "scale": 0.1, "unit": "VA", "description": "Grid output power HIGH", "pair": 41},
    41: {"name": "Grid_Power_L", "scale": 0.1, "unit": "VA", "description": "Grid output power LOW", "pair": 40},
    
    # Three Phase Grid (if applicable)
    42: {"name": "Vac2", "scale": 0.1, "unit": "V", "description": "Phase 2 voltage (3-phase only)"},
    43: {"name": "Iac2", "scale": 0.1, "unit": "A", "description": "Phase 2 current (3-phase only)"},
    44: {"name": "Pac2_H", "scale": 0.1, "unit": "VA", "description": "Phase 2 power HIGH", "pair": 45},
    45: {"name": "Pac2_L", "scale": 0.1, "unit": "VA", "description": "Phase 2 power LOW", "pair": 44},
    46: {"name": "Vac3", "scale": 0.1, "unit": "V", "description": "Phase 3 voltage (3-phase only)"},
    47: {"name": "Iac3", "scale": 0.1, "unit": "A", "description": "Phase 3 current (3-phase only)"},
    48: {"name": "Pac3_H", "scale": 0.1, "unit": "VA", "description": "Phase 3 power HIGH", "pair": 49},
    49: {"name": "Pac3_L", "scale": 0.1, "unit": "VA", "description": "Phase 3 power LOW", "pair": 48},
    
    # Line Voltages (3-phase)
    50: {"name": "Vac_RS", "scale": 0.1, "unit": "V", "description": "Line voltage R-S"},
    51: {"name": "Vac_ST", "scale": 0.1, "unit": "V", "description": "Line voltage S-T"},
    52: {"name": "Vac_TR", "scale": 0.1, "unit": "V", "description": "Line voltage T-R"},
    
    # Energy
    53: {"name": "Energy_Today_H", "scale": 0.1, "unit": "kWh", "description": "Today energy HIGH", "pair": 54},
    54: {"name": "Energy_Today_L", "scale": 0.1, "unit": "kWh", "description": "Today energy LOW", "pair": 53},
    55: {"name": "Energy_Total_H", "scale": 0.1, "unit": "kWh", "description": "Total lifetime energy HIGH", "pair": 56},
    56: {"name": "Energy_Total_L", "scale": 0.1, "unit": "kWh", "description": "Total lifetime energy LOW", "pair": 55},
    
    # Operating Time
    57: {"name": "Time_Total_H", "scale": 0.5, "unit": "s", "description": "Total operating time HIGH", "pair": 58},
    58: {"name": "Time_Total_L", "scale": 0.5, "unit": "s", "description": "Total operating time LOW", "pair": 57},
    
    # PV Energy by String
    59: {"name": "PV1_Energy_Today_H", "scale": 0.1, "unit": "kWh", "pair": 60},
    60: {"name": "PV1_Energy_Today_L", "scale": 0.1, "unit": "kWh", "pair": 59},
    61: {"name": "PV1_Energy_Total_H", "scale": 0.1, "unit": "kWh", "pair": 62},
    62: {"name": "PV1_Energy_Total_L", "scale": 0.1, "unit": "kWh", "pair": 61},
    63: {"name": "PV2_Energy_Today_H", "scale": 0.1, "unit": "kWh", "pair": 64},
    64: {"name": "PV2_Energy_Today_L", "scale": 0.1, "unit": "kWh", "pair": 63},
    65: {"name": "PV2_Energy_Total_H", "scale": 0.1, "unit": "kWh", "pair": 66},
    66: {"name": "PV2_Energy_Total_L", "scale": 0.1, "unit": "kWh", "pair": 65},
    
    # Temperatures
    93: {"name": "Inverter_Temp", "scale": 0.1, "unit": "°C", "description": "Inverter temperature"},
    94: {"name": "IPM_Temp", "scale": 0.1, "unit": "°C", "description": "IPM (power module) temperature"},
    95: {"name": "Boost_Temp", "scale": 0.1, "unit": "°C", "description": "Boost converter temperature"},
    
    # Internal Voltages
    98: {"name": "P_Bus_Voltage", "scale": 0.1, "unit": "V", "description": "Positive bus voltage"},
    99: {"name": "N_Bus_Voltage", "scale": 0.1, "unit": "V", "description": "Negative bus voltage"},
    
    # Power Factor
    100: {"name": "Power_Factor", "scale": 1, "unit": "", "description": "0-10000=underexcited, 10001-20000=overexcited"},
    
    # Diagnostics
    104: {"name": "Derating_Mode", "scale": 1, "unit": "", "description": "See derating table"},
    105: {"name": "Fault_Code", "scale": 1, "unit": "", "description": "Main fault code"},
    107: {"name": "Fault_Subcode", "scale": 1, "unit": "", "description": "Fault subcode"},
    110: {"name": "Warning_H", "scale": 1, "unit": "", "description": "Warning bits HIGH"},
    111: {"name": "Warning_Subcode", "scale": 1, "unit": "", "description": "Warning subcode"},
    112: {"name": "Warning_Code", "scale": 1, "unit": "", "description": "Main warning code"},
}

# INPUT REGISTERS (Function Code 0x04) - Storage/Hybrid Range 3000-3124
INPUT_REGISTERS_STORAGE = {
    # System Status
    3000: {"name": "System_Status", "scale": 1, "unit": "", "description": "High 8 bits=mode, Low 8 bits=status"},
    
    # PV Input (same as base but at 3000 offset)
    3001: {"name": "PV_Total_Power_H", "scale": 0.1, "unit": "W", "pair": 3002},
    3002: {"name": "PV_Total_Power_L", "scale": 0.1, "unit": "W", "pair": 3001},
    3003: {"name": "PV1_Voltage", "scale": 0.1, "unit": "V"},
    3004: {"name": "PV1_Current", "scale": 0.1, "unit": "A"},
    3005: {"name": "PV1_Power_H", "scale": 0.1, "unit": "W", "pair": 3006},
    3006: {"name": "PV1_Power_L", "scale": 0.1, "unit": "W", "pair": 3005},
    3007: {"name": "PV2_Voltage", "scale": 0.1, "unit": "V"},
    3008: {"name": "PV2_Current", "scale": 0.1, "unit": "A"},
    3009: {"name": "PV2_Power_H", "scale": 0.1, "unit": "W", "pair": 3010},
    3010: {"name": "PV2_Power_L", "scale": 0.1, "unit": "W", "pair": 3009},
    
    # System Power
    3019: {"name": "System_Output_Power_H", "scale": 0.1, "unit": "W", "pair": 3020},
    3020: {"name": "System_Output_Power_L", "scale": 0.1, "unit": "W", "pair": 3019},
    3021: {"name": "Reactive_Power_H", "scale": 0.1, "unit": "var", "pair": 3022},
    3022: {"name": "Reactive_Power_L", "scale": 0.1, "unit": "var", "pair": 3021},
    3023: {"name": "Output_Power_H", "scale": 0.1, "unit": "W", "pair": 3024},
    3024: {"name": "Output_Power_L", "scale": 0.1, "unit": "W", "pair": 3023},
    
    # AC Output (THIS IS KEY - Different from Grid!)
    3025: {"name": "AC_Frequency", "scale": 0.01, "unit": "Hz", "description": "Inverter AC output frequency"},
    3026: {"name": "AC_Voltage", "scale": 0.1, "unit": "V", "description": "Inverter AC output voltage"},
    3027: {"name": "AC_Current", "scale": 0.1, "unit": "A", "description": "Inverter AC output current"},
    3028: {"name": "AC_Power_H", "scale": 0.1, "unit": "VA", "pair": 3029},
    3029: {"name": "AC_Power_L", "scale": 0.1, "unit": "VA", "pair": 3028},
    
    # Power Flow
    3041: {"name": "Power_To_User_H", "scale": 0.1, "unit": "W", "description": "Forward power HIGH", "pair": 3042},
    3042: {"name": "Power_To_User_L", "scale": 0.1, "unit": "W", "description": "Forward power LOW", "pair": 3041},
    3043: {"name": "Power_To_Grid_H", "scale": 0.1, "unit": "W", "description": "Reverse/export power HIGH", "pair": 3044},
    3044: {"name": "Power_To_Grid_L", "scale": 0.1, "unit": "W", "description": "Reverse/export power LOW", "pair": 3043},
    3045: {"name": "Power_To_Load_H", "scale": 0.1, "unit": "W", "description": "Load power HIGH", "pair": 3046},
    3046: {"name": "Power_To_Load_L", "scale": 0.1, "unit": "W", "description": "Load power LOW", "pair": 3045},
    
    # Operating Time
    3047: {"name": "Time_Total_H", "scale": 0.5, "unit": "s", "pair": 3048},
    3048: {"name": "Time_Total_L", "scale": 0.5, "unit": "s", "pair": 3047},
    
    # Energy Totals
    3049: {"name": "Energy_Today_H", "scale": 0.1, "unit": "kWh", "pair": 3050},
    3050: {"name": "Energy_Today_L", "scale": 0.1, "unit": "kWh", "pair": 3049},
    3051: {"name": "Energy_Total_H", "scale": 0.1, "unit": "kWh", "pair": 3052},
    3052: {"name": "Energy_Total_L", "scale": 0.1, "unit": "kWh", "pair": 3051},
    
    # Energy Breakdown
    3067: {"name": "Energy_To_User_Today_H", "scale": 0.1, "unit": "kWh", "pair": 3068},
    3068: {"name": "Energy_To_User_Today_L", "scale": 0.1, "unit": "kWh", "pair": 3067},
    3069: {"name": "Energy_To_User_Total_H", "scale": 0.1, "unit": "kWh", "pair": 3070},
    3070: {"name": "Energy_To_User_Total_L", "scale": 0.1, "unit": "kWh", "pair": 3069},
    3071: {"name": "Energy_To_Grid_Today_H", "scale": 0.1, "unit": "kWh", "pair": 3072},
    3072: {"name": "Energy_To_Grid_Today_L", "scale": 0.1, "unit": "kWh", "pair": 3071},
    3073: {"name": "Energy_To_Grid_Total_H", "scale": 0.1, "unit": "kWh", "pair": 3074},
    3074: {"name": "Energy_To_Grid_Total_L", "scale": 0.1, "unit": "kWh", "pair": 3073},
    3075: {"name": "Load_Energy_Today_H", "scale": 0.1, "unit": "kWh", "pair": 3076},
    3076: {"name": "Load_Energy_Today_L", "scale": 0.1, "unit": "kWh", "pair": 3075},
    3077: {"name": "Load_Energy_Total_H", "scale": 0.1, "unit": "kWh", "pair": 3078},
    3078: {"name": "Load_Energy_Total_L", "scale": 0.1, "unit": "kWh", "pair": 3077},
    
    # Diagnostics
    3086: {"name": "Derating_Mode", "scale": 1, "unit": ""},
    3087: {"name": "PV_ISO", "scale": 1, "unit": "kΩ", "description": "PV isolation resistance"},
    3088: {"name": "DCI_R", "scale": 0.1, "unit": "mA", "description": "DC injection R phase"},
    3091: {"name": "GFCI", "scale": 1, "unit": "mA", "description": "Ground fault current"},
    3092: {"name": "Bus_Voltage", "scale": 0.1, "unit": "V"},
    
    # Temperatures
    3093: {"name": "Inverter_Temp", "scale": 0.1, "unit": "°C"},
    3094: {"name": "IPM_Temp", "scale": 0.1, "unit": "°C"},
    3095: {"name": "Boost_Temp", "scale": 0.1, "unit": "°C"},
    3097: {"name": "Comms_Board_Temp", "scale": 0.1, "unit": "°C"},
    
    # Faults
    3105: {"name": "Fault_Code", "scale": 1, "unit": ""},
    3106: {"name": "Warning_Code", "scale": 1, "unit": ""},
    3107: {"name": "Fault_Subcode", "scale": 1, "unit": ""},
    3108: {"name": "Warning_Subcode", "scale": 1, "unit": ""},
}

# HOLDING REGISTERS (Function Code 0x03) - Configuration (mostly read-only for normal use)
HOLDING_REGISTERS = {
    0: {"name": "OnOff", "scale": 1, "unit": "", "access": "RW", "description": "0=Off, 1=On"},
    3: {"name": "Active_Power_Rate", "scale": 1, "unit": "%", "access": "RW", "description": "Max output power %"},
    15: {"name": "LCD_Language", "scale": 1, "unit": "", "access": "RW"},
    22: {"name": "Baud_Rate", "scale": 1, "unit": "", "access": "RW", "description": "0=9600, 1=38400"},
    30: {"name": "Com_Address", "scale": 1, "unit": "", "access": "RW", "description": "Modbus address 1-254"},
    45: {"name": "Sys_Year", "scale": 1, "unit": "", "access": "RW"},
    46: {"name": "Sys_Month", "scale": 1, "unit": "", "access": "RW"},
    47: {"name": "Sys_Day", "scale": 1, "unit": "", "access": "RW"},
    48: {"name": "Sys_Hour", "scale": 1, "unit": "", "access": "RW"},
    49: {"name": "Sys_Min", "scale": 1, "unit": "", "access": "RW"},
    50: {"name": "Sys_Sec", "scale": 1, "unit": "", "access": "RW"},
}

# Helper function to combine 32-bit registers
def combine_registers(high, low):
    """Combine two 16-bit registers into 32-bit value"""
    return (high << 16) | low

# Helper function to calculate scaled value
def scale_value(raw_value, scale):
    """Apply scaling factor to raw register value"""
    return raw_value * scale

# Example usage
if __name__ == "__main__":
    # Example: Reading grid voltage from register 38
    raw_value = 2345  # Example raw value
    reg_info = INPUT_REGISTERS_BASE[38]
    scaled = scale_value(raw_value, reg_info["scale"])
    print(f"{reg_info['name']}: {scaled} {reg_info['unit']}")
    # Output: Grid_Voltage: 234.5 V
    
    # Example: Combining 32-bit power reading
    power_h = 156  # Example HIGH word
    power_l = 18240  # Example LOW word
    combined = combine_registers(power_h, power_l)
    scaled_power = scale_value(combined, 0.1)
    print(f"Total Power: {scaled_power} W")