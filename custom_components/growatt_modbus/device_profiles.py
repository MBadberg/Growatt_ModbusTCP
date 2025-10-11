"""
Device profiles for different Growatt inverter series.
Each profile defines which sensors and features are available.
"""

from typing import Dict, List, Set

# Device profile structure
class InverterProfile:
    """Profile for a specific inverter series."""
    
    def __init__(
        self,
        series: str,
        name: str,
        description: str,
        register_map: str,
        available_sensors: Set[str],
        phases: int = 1,
        has_battery: bool = False,
        has_pv3: bool = False,
        max_power_kw: float = 10.0,
    ):
        """Initialize inverter profile."""
        self.series = series
        self.name = name
        self.description = description
        self.register_map = register_map
        self.available_sensors = available_sensors
        self.phases = phases
        self.has_battery = has_battery
        self.has_pv3 = has_pv3
        self.max_power_kw = max_power_kw


# Common sensor sets for reuse
BASIC_PV_SENSORS = {
    "pv1_voltage", "pv1_current", "pv1_power",
    "pv2_voltage", "pv2_current", "pv2_power",
    "pv_total_power",
}

PV3_SENSORS = {
    "pv3_voltage", "pv3_current", "pv3_power",
}

BASIC_AC_SENSORS = {
    "ac_voltage", "ac_current", "ac_power", "ac_frequency",
}

GRID_SENSORS = {
    "grid_power", "grid_export_power", "grid_import_power",
}

POWER_FLOW_SENSORS = {
    "power_to_grid", "power_to_load", "power_to_user",
}

CONSUMPTION_SENSORS = {
    "self_consumption", "self_consumption_percentage", "house_consumption",
}

ENERGY_SENSORS = {
    "energy_today", "energy_total",
}

ENERGY_BREAKDOWN_SENSORS = {
    "grid_energy_today", "grid_energy_total",
    "energy_to_grid_today", "energy_to_grid_total",
    "grid_import_energy_today", "grid_import_energy_total",
    "load_energy_today", "load_energy_total",
}

TEMPERATURE_SENSORS = {
    "inverter_temp", "ipm_temp", "boost_temp",
}

STATUS_SENSORS = {
    "status", "last_update", "derating_mode", "fault_code", "warning_code",
}

BATTERY_SENSORS = {
    "battery_voltage", "battery_current", "battery_power",
    "battery_soc", "battery_temp",
    "battery_charge_today", "battery_discharge_today",
    "battery_charge_total", "battery_discharge_total",
    "priority_mode", "battery_derating_mode",
}

THREE_PHASE_SENSORS = {
    "ac_voltage_r", "ac_voltage_s", "ac_voltage_t",
    "ac_current_r", "ac_current_s", "ac_current_t",
    "ac_power_r", "ac_power_s", "ac_power_t",
}


# ============================================================================
# MIN SERIES - Single Phase String Inverters (3-10kW)
# ============================================================================

MIN_3000_6000_TL_X = InverterProfile(
    series="min_3000_6000_tl_x",
    name="MIN 3000-6000TL-X",
    description="MIN series 3kW-6kW single-phase string inverters (2 PV inputs)",
    register_map="MIN_3000_6000TL_X",
    available_sensors=(
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
    phases=1,
    has_battery=False,
    has_pv3=False,
    max_power_kw=6.0,
)

MIN_7000_10000_TL_X = InverterProfile(
    series="min_7000_10000_tl_x",
    name="MIN 7000-10000TL-X",
    description="MIN series 7kW-10kW single-phase string inverters (3 PV inputs)",
    register_map="MIN_7000_10000TL_X",
    available_sensors=(
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
    phases=1,
    has_battery=False,
    has_pv3=True,
    max_power_kw=10.0,
)


# ============================================================================
# MID SERIES - Three Phase String Inverters (15-25kW)
# ============================================================================

MID_15000_25000_TL3_X = InverterProfile(
    series="mid_15000_25000_tl3_x",
    name="MID 15000-25000TL3-X",
    description="MID series 15kW-25kW three-phase string inverters",
    register_map="MID_15000_25000TL3_X",
    available_sensors=(
        BASIC_PV_SENSORS |
        PV3_SENSORS |
        BASIC_AC_SENSORS |
        THREE_PHASE_SENSORS |
        GRID_SENSORS |
        POWER_FLOW_SENSORS |
        CONSUMPTION_SENSORS |
        ENERGY_SENSORS |
        ENERGY_BREAKDOWN_SENSORS |
        TEMPERATURE_SENSORS |
        STATUS_SENSORS
    ),
    phases=3,
    has_battery=False,
    has_pv3=True,
    max_power_kw=25.0,
)


# ============================================================================
# MAX SERIES - Commercial Three Phase (50-125kW)
# ============================================================================

MAX_50000_125000_TL3_X = InverterProfile(
    series="max_50000_125000_tl3_x",
    name="MAX 50000-125000TL3-X",
    description="MAX series 50kW-125kW commercial three-phase inverters",
    register_map="MAX_50000_125000TL3_X",
    available_sensors=(
        BASIC_PV_SENSORS |
        PV3_SENSORS |
        BASIC_AC_SENSORS |
        THREE_PHASE_SENSORS |
        GRID_SENSORS |
        POWER_FLOW_SENSORS |
        CONSUMPTION_SENSORS |
        ENERGY_SENSORS |
        ENERGY_BREAKDOWN_SENSORS |
        TEMPERATURE_SENSORS |
        STATUS_SENSORS
    ),
    phases=3,
    has_battery=False,
    has_pv3=True,
    max_power_kw=125.0,
)


# ============================================================================
# SPH SERIES - Hybrid Storage Inverters (3-10kW)
# ============================================================================

SPH_3000_10000 = InverterProfile(
    series="sph_3000_10000",
    name="SPH 3000-10000",
    description="SPH series 3kW-10kW single-phase hybrid inverters with battery",
    register_map="SPH_3000_10000",
    available_sensors=(
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
    phases=1,
    has_battery=True,
    has_pv3=True,
    max_power_kw=10.0,
)


# ============================================================================
# MOD SERIES - Modular Three Phase with Battery (6-15kW)
# ============================================================================

MOD_6000_15000_TL3_XH = InverterProfile(
    series="mod_6000_15000_tl3_xh",
    name="MOD 6000-15000TL3-XH",
    description="MOD series 6kW-15kW three-phase hybrid inverters with battery",
    register_map="MOD_6000_15000TL3_XH",
    available_sensors=(
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
    phases=3,
    has_battery=True,
    has_pv3=True,
    max_power_kw=15.0,
)


# ============================================================================
# PROFILE REGISTRY
# ============================================================================

INVERTER_PROFILES: Dict[str, InverterProfile] = {
    # MIN Series
    "min_3000_6000_tl_x": MIN_3000_6000_TL_X,
    "min_7000_10000_tl_x": MIN_7000_10000_TL_X,
    
    # MID Series
    "mid_15000_25000_tl3_x": MID_15000_25000_TL3_X,
    
    # MAX Series
    "max_50000_125000_tl3_x": MAX_50000_125000_TL3_X,
    
    # SPH Series (Hybrid/Storage)
    "sph_3000_10000": SPH_3000_10000,
    
    # MOD Series (Modular Hybrid)
    "mod_6000_15000_tl3_xh": MOD_6000_15000_TL3_XH,
}


def get_profile(series: str) -> InverterProfile:
    """Get inverter profile by series name."""
    return INVERTER_PROFILES.get(series)


def get_available_profiles() -> Dict[str, str]:
    """Get dict of available profiles for UI selection."""
    return {
        series: profile.name 
        for series, profile in INVERTER_PROFILES.items()
    }


def get_sensors_for_profile(series: str) -> Set[str]:
    """Get available sensors for a specific profile."""
    profile = get_profile(series)
    if profile:
        return profile.available_sensors
    return set()


def profile_supports_sensor(series: str, sensor_key: str) -> bool:
    """Check if a profile supports a specific sensor."""
    profile = get_profile(series)
    if profile:
        return sensor_key in profile.available_sensors
    return False