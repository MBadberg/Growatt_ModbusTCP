"""Device profiles for Growatt inverters."""
from typing import Dict, Set


# ============================================================================
# SENSOR GROUPS
# ============================================================================

BASIC_PV_SENSORS: Set[str] = {
    "pv1_voltage", "pv1_current", "pv1_power",
    "pv2_voltage", "pv2_current", "pv2_power",
    "pv_total_power",
}

PV3_SENSORS: Set[str] = {
    "pv3_voltage", "pv3_current", "pv3_power",
}

BASIC_AC_SENSORS: Set[str] = {
    "ac_voltage", "ac_current", "ac_power", "ac_frequency",
}

GRID_SENSORS: Set[str] = {
    "grid_power", "grid_export_power", "grid_import_power",
}

POWER_FLOW_SENSORS: Set[str] = {
    "power_to_grid", "power_to_load", "power_to_user",
}

CONSUMPTION_SENSORS: Set[str] = {
    "self_consumption", "self_consumption_percentage", "house_consumption",
}

ENERGY_SENSORS: Set[str] = {
    "energy_today", "energy_total",
}

ENERGY_BREAKDOWN_SENSORS: Set[str] = {
    "grid_energy_today", "grid_energy_total",
    "energy_to_grid_today", "energy_to_grid_total",
    "grid_import_energy_today", "grid_import_energy_total",
    "load_energy_today", "load_energy_total",
}

BATTERY_SENSORS: Set[str] = {
    "battery_voltage", "battery_current", "battery_soc",
    "battery_temp", "battery_power",
    "battery_charge_power", "battery_discharge_power",
    "battery_charge_today", "battery_discharge_today",
    "battery_charge_total", "battery_discharge_total",
}

TEMPERATURE_SENSORS: Set[str] = {
    "inverter_temp", "ipm_temp", "boost_temp",
}

STATUS_SENSORS: Set[str] = {
    "status", "last_update", "derating_mode", "fault_code", "warning_code",
}

THREE_PHASE_SENSORS: Set[str] = {
    "ac_voltage_r", "ac_voltage_s", "ac_voltage_t",
    "ac_current_r", "ac_current_s", "ac_current_t",
    "ac_power_r", "ac_power_s", "ac_power_t",
}


# ============================================================================
# INVERTER PROFILES
# ============================================================================

INVERTER_PROFILES = {
    # ========================================================================
    # MIN SERIES - Single Phase String Inverters
    # ========================================================================
    
    "min_3000_6000_tl_x": {
        "name": "MIN 3000-6000TL-X",
        "description": "2 PV string single-phase inverter (3-6kW)",
        "register_map": "MIN_3000_6000TL_X",
        "phases": 1,
        "has_pv3": False,
        "has_battery": False,
        "max_power_kw": 6.0,
        "sensors": (
            BASIC_PV_SENSORS |
            BASIC_AC_SENSORS |
            GRID_SENSORS |
            POWER_FLOW_SENSORS |
            CONSUMPTION_SENSORS |
            ENERGY_SENSORS |
            ENERGY_BREAKDOWN_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    "min_7000_10000_tl_x": {
        "name": "MIN 7000-10000TL-X",
        "description": "3 PV string single-phase inverter (7-10kW)",
        "register_map": "MIN_7000_10000TL_X",
        "phases": 1,
        "has_pv3": True,
        "has_battery": False,
        "max_power_kw": 10.0,
        "sensors": (
            BASIC_PV_SENSORS |
            PV3_SENSORS |
            BASIC_AC_SENSORS |
            GRID_SENSORS |
            POWER_FLOW_SENSORS |
            CONSUMPTION_SENSORS |
            ENERGY_SENSORS |
            ENERGY_BREAKDOWN_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    # ========================================================================
    # TL-XH SERIES - Single Phase Hybrid (with battery)
    # ========================================================================
    
    "tl_xh_3000_10000": {
        "name": "TL-XH 3000-10000",
        "description": "Hybrid single-phase inverter with battery (3-10kW)",
        "register_map": "TL_XH_3000_10000",
        "phases": 1,
        "has_pv3": True,
        "has_battery": True,
        "max_power_kw": 10.0,
        "sensors": (
            BASIC_PV_SENSORS |
            PV3_SENSORS |
            BASIC_AC_SENSORS |
            GRID_SENSORS |
            POWER_FLOW_SENSORS |
            CONSUMPTION_SENSORS |
            ENERGY_SENSORS |
            ENERGY_BREAKDOWN_SENSORS |
            BATTERY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    "tl_xh_us_3000_10000": {
        "name": "TL-XH US 3000-10000",
        "description": "US hybrid single-phase inverter with battery (3-10kW)",
        "register_map": "TL_XH_US_3000_10000",
        "phases": 1,
        "has_pv3": True,
        "has_battery": True,
        "max_power_kw": 10.0,
        "sensors": (
            BASIC_PV_SENSORS |
            PV3_SENSORS |
            BASIC_AC_SENSORS |
            GRID_SENSORS |
            POWER_FLOW_SENSORS |
            CONSUMPTION_SENSORS |
            ENERGY_SENSORS |
            ENERGY_BREAKDOWN_SENSORS |
            BATTERY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    # ========================================================================
    # MID SERIES - Three Phase String Inverters
    # ========================================================================
    
    "mid_15000_25000tl3_x": {
        "name": "MID 15000-25000TL3-X",
        "description": "Three-phase commercial inverter (15-25kW)",
        "register_map": "MID_15000_25000TL3_X",
        "phases": 3,
        "has_pv3": False,
        "has_battery": False,
        "max_power_kw": 25.0,
        "sensors": (
            BASIC_PV_SENSORS |
            BASIC_AC_SENSORS |
            THREE_PHASE_SENSORS |
            ENERGY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    # ========================================================================
    # MAC SERIES - Three Phase Compact
    # ========================================================================
    
    "mac_20000_40000tl3_x": {
        "name": "MAC 20000-40000TL3-X",
        "description": "Compact three-phase commercial inverter (20-40kW)",
        "register_map": "MAC_20000_40000TL3_X",
        "phases": 3,
        "has_pv3": False,
        "has_battery": False,
        "max_power_kw": 40.0,
        "sensors": (
            BASIC_PV_SENSORS |
            BASIC_AC_SENSORS |
            THREE_PHASE_SENSORS |
            ENERGY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    # ========================================================================
    # MAX SERIES - Commercial Three Phase
    # ========================================================================
    
    "max_50000_125000tl3_x": {
        "name": "MAX 50000-125000TL3-X",
        "description": "Commercial three-phase inverter (50-125kW)",
        "register_map": "MAX_50000_125000TL3_X",
        "phases": 3,
        "has_pv3": True,
        "has_battery": False,
        "max_power_kw": 125.0,
        "sensors": (
            BASIC_PV_SENSORS |
            PV3_SENSORS |
            BASIC_AC_SENSORS |
            THREE_PHASE_SENSORS |
            ENERGY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    "max_1500v_series": {
        "name": "MAX 1500V Series",
        "description": "High-voltage commercial three-phase inverter (up to 150kW)",
        "register_map": "MAX_1500V_SERIES",
        "phases": 3,
        "has_pv3": True,
        "has_battery": False,
        "max_power_kw": 150.0,
        "sensors": (
            BASIC_PV_SENSORS |
            PV3_SENSORS |
            BASIC_AC_SENSORS |
            THREE_PHASE_SENSORS |
            ENERGY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    "max_x_lv_series": {
        "name": "MAX-X LV Series",
        "description": "Low-voltage commercial three-phase inverter (up to 125kW)",
        "register_map": "MAX_X_LV_SERIES",
        "phases": 3,
        "has_pv3": True,
        "has_battery": False,
        "max_power_kw": 125.0,
        "sensors": (
            BASIC_PV_SENSORS |
            PV3_SENSORS |
            BASIC_AC_SENSORS |
            THREE_PHASE_SENSORS |
            ENERGY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    # ========================================================================
    # SPH SERIES - Hybrid Storage (Three Phase with Battery)
    # ========================================================================
    
    "sph_3000_10000": {
        "name": "SPH 3000-10000",
        "description": "Three-phase hybrid inverter with battery storage (3-10kW, includes SPH 10000 TL3 BH UP)",
        "register_map": "SPH_3000_10000",
        "phases": 3,  # Three-phase (TL3 = Three Level/Line 3-phase)
        "has_pv3": False,  # SPH typically has 2 PV inputs
        "has_battery": True,
        "max_power_kw": 10.0,
        "sensors": (
            BASIC_PV_SENSORS |
            BASIC_AC_SENSORS |
            THREE_PHASE_SENSORS |  # Added three-phase sensor support
            GRID_SENSORS |
            POWER_FLOW_SENSORS |
            CONSUMPTION_SENSORS |
            ENERGY_SENSORS |
            ENERGY_BREAKDOWN_SENSORS |
            BATTERY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    # ========================================================================
    # MIX SERIES - Legacy Storage
    # ========================================================================
    
    "mix_series": {
        "name": "MIX Series",
        "description": "Legacy storage inverter (merged into SPH)",
        "register_map": "MIX_SERIES",
        "phases": 1,
        "has_pv3": False,
        "has_battery": True,
        "max_power_kw": 10.0,
        "sensors": (
            BASIC_PV_SENSORS |
            BASIC_AC_SENSORS |
            GRID_SENSORS |
            POWER_FLOW_SENSORS |
            CONSUMPTION_SENSORS |
            ENERGY_SENSORS |
            ENERGY_BREAKDOWN_SENSORS |
            BATTERY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    # ========================================================================
    # SPA SERIES - AC-Coupled Storage
    # ========================================================================
    
    "spa_series": {
        "name": "SPA Series",
        "description": "AC-coupled storage inverter",
        "register_map": "SPA_SERIES",
        "phases": 1,
        "has_pv3": False,
        "has_battery": True,
        "max_power_kw": 10.0,
        "sensors": (
            GRID_SENSORS |
            POWER_FLOW_SENSORS |
            CONSUMPTION_SENSORS |
            ENERGY_SENSORS |
            ENERGY_BREAKDOWN_SENSORS |
            BATTERY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    # ========================================================================
    # MOD SERIES - Modular Three Phase Hybrid
    # ========================================================================
    
    "mod_6000_15000tl3_xh": {
        "name": "MOD 6000-15000TL3-XH",
        "description": "Modular three-phase hybrid inverter with battery (6-15kW)",
        "register_map": "MOD_6000_15000TL3_XH",
        "phases": 3,
        "has_pv3": True,
        "has_battery": True,
        "max_power_kw": 15.0,
        "sensors": (
            BASIC_PV_SENSORS |
            PV3_SENSORS |
            BASIC_AC_SENSORS |
            THREE_PHASE_SENSORS |
            GRID_SENSORS |
            POWER_FLOW_SENSORS |
            CONSUMPTION_SENSORS |
            ENERGY_SENSORS |
            ENERGY_BREAKDOWN_SENSORS |
            BATTERY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
    
    # ========================================================================
    # WIT SERIES - Business Storage Power
    # ========================================================================
    
    "wit_tl3_series": {
        "name": "WIT TL3 Series",
        "description": "Business storage power three-phase inverter",
        "register_map": "WIT_TL3_SERIES",
        "phases": 3,
        "has_pv3": True,
        "has_battery": True,
        "max_power_kw": 50.0,
        "sensors": (
            BASIC_PV_SENSORS |
            PV3_SENSORS |
            BASIC_AC_SENSORS |
            THREE_PHASE_SENSORS |
            GRID_SENSORS |
            POWER_FLOW_SENSORS |
            CONSUMPTION_SENSORS |
            ENERGY_SENSORS |
            ENERGY_BREAKDOWN_SENSORS |
            BATTERY_SENSORS |
            TEMPERATURE_SENSORS |
            STATUS_SENSORS
        ),
    },
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_profile(series: str):
    """Get inverter profile by series name."""
    return INVERTER_PROFILES.get(series, INVERTER_PROFILES["min_7000_10000_tl_x"])


def get_available_profiles() -> Dict[str, str]:
    """Get dict of available profiles for UI selection."""
    return {
        series: profile["name"]
        for series, profile in INVERTER_PROFILES.items()
    }


def get_sensors_for_profile(series: str) -> Set[str]:
    """Get available sensors for a profile."""
    profile = get_profile(series)
    return profile.get("sensors", set())