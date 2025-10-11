"""Diagnostic service for Growatt Modbus Integration."""
import asyncio
import logging
from typing import Any

import voluptuous as vol
from pymodbus.client import ModbusTcpClient

from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Service name
SERVICE_DIAGNOSTIC = "run_diagnostic"

# Test profiles with key registers
DIAGNOSTIC_PROFILES = {
    "min_3000_6000_tl_x": {
        "name": "MIN 3000-6000TL-X",
        "registers": [
            (3000, "Status", 1, ""),
            (3003, "PV1 Voltage", 0.1, "V"),
            (3007, "PV2 Voltage", 0.1, "V"),
            (3026, "AC Voltage", 0.1, "V"),
            (3025, "AC Frequency", 0.01, "Hz"),
        ],
    },
    "min_7000_10000_tl_x": {
        "name": "MIN 7000-10000TL-X",
        "registers": [
            (3000, "Status", 1, ""),
            (3003, "PV1 Voltage", 0.1, "V"),
            (3007, "PV2 Voltage", 0.1, "V"),
            (3011, "PV3 Voltage", 0.1, "V"),
            (3026, "AC Voltage", 0.1, "V"),
        ],
    },
    "sph_3000_10000": {
        "name": "SPH 3000-10000",
        "registers": [
            (0, "Status (Base)", 1, ""),
            (3, "PV1 Voltage", 0.1, "V"),
            (7, "PV2 Voltage", 0.1, "V"),
            (38, "AC Voltage", 0.1, "V"),
            (1013, "Battery Voltage", 0.1, "V"),
            (1014, "Battery SOC", 1, "%"),
        ],
    },
    "mid_15000_25000tl3_x": {
        "name": "MID 15000-25000TL3-X",
        "registers": [
            (0, "Status", 1, ""),
            (3, "PV1 Voltage", 0.1, "V"),
            (38, "Grid Voltage R", 0.1, "V"),
            (42, "Grid Voltage S", 0.1, "V"),
            (37, "Grid Frequency", 0.01, "Hz"),
        ],
    },
    "mod_6000_15000tl3_xh": {
        "name": "MOD 6000-15000TL3-XH",
        "registers": [
            (3000, "Status", 1, ""),
            (3003, "PV1 Voltage", 0.1, "V"),
            (3026, "AC Voltage R", 0.1, "V"),
            (3169, "Battery Voltage", 0.01, "V"),
            (3171, "Battery SOC", 1, "%"),
        ],
    },
}

# Service schema
SERVICE_DIAGNOSTIC_SCHEMA = vol.Schema(
    {
        vol.Required("host"): cv.string,
        vol.Optional("port", default=502): cv.port,
        vol.Optional("slave_id", default=1): vol.All(vol.Coerce(int), vol.Range(min=1, max=247)),
        vol.Required("inverter_series"): vol.In(list(DIAGNOSTIC_PROFILES.keys())),
        vol.Optional("notify", default=True): cv.boolean,
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up diagnostic services."""

    async def run_diagnostic(call: ServiceCall) -> None:
        """Run diagnostic test on inverter."""
        host = call.data["host"]
        port = call.data["port"]
        slave_id = call.data["slave_id"]
        series = call.data["inverter_series"]
        send_notification = call.data["notify"]

        profile = DIAGNOSTIC_PROFILES[series]
        
        _LOGGER.info("Starting diagnostic for %s at %s:%s", profile["name"], host, port)

        # Run test in executor (blocking I/O)
        result = await hass.async_add_executor_job(
            _test_connection, host, port, slave_id, profile
        )

        # Log results
        _LOGGER.info("Diagnostic complete: %s", result["summary"])
        for line in result["details"]:
            _LOGGER.info(line)

        # Send notification if requested
        if send_notification:
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": f"🔌 Growatt Diagnostic: {profile['name']}",
                    "message": _format_notification(result),
                    "notification_id": "growatt_diagnostic",
                },
            )

    hass.services.async_register(
        DOMAIN,
        SERVICE_DIAGNOSTIC,
        run_diagnostic,
        schema=SERVICE_DIAGNOSTIC_SCHEMA,
    )


def _test_connection(host: str, port: int, slave_id: int, profile: dict) -> dict:
    """Test connection and read registers (blocking)."""
    results = {
        "success": False,
        "connected": False,
        "total": len(profile["registers"]),
        "passed": 0,
        "details": [],
        "summary": "",
    }

    # Test TCP connection
    try:
        client = ModbusTcpClient(host=host, port=port, timeout=5)
        if not client.connect():
            results["summary"] = "❌ Failed to connect"
            results["details"].append(f"Cannot connect to {host}:{port}")
            return results
        
        results["connected"] = True
        results["details"].append(f"✅ Connected to {host}:{port}")

    except Exception as e:
        results["summary"] = f"❌ Connection error: {e}"
        results["details"].append(f"Error: {e}")
        return results

    # Test each register
    try:
        for address, name, scale, unit in profile["registers"]:
            try:
                result = client.read_input_registers(address=address, count=1, device_id=slave_id)
                
                if result.isError():
                    results["details"].append(f"❌ Register {address} ({name}): Read error")
                else:
                    raw = result.registers[0]
                    scaled = raw * scale
                    
                    # Format value
                    if "Status" in name:
                        status_map = {0: "Waiting", 1: "Normal", 3: "Fault"}
                        value_str = status_map.get(scaled, f"Unknown ({scaled})")
                    else:
                        value_str = f"{scaled:.2f} {unit}" if unit else f"{scaled}"
                    
                    results["details"].append(f"✅ Register {address} ({name}): {value_str}")
                    results["passed"] += 1
                    
            except Exception as e:
                results["details"].append(f"❌ Register {address} ({name}): {e}")

    finally:
        client.close()

    # Summary
    if results["passed"] == results["total"]:
        results["success"] = True
        results["summary"] = f"✅ All tests passed ({results['passed']}/{results['total']})"
    elif results["passed"] > 0:
        results["summary"] = f"⚠️ Partial success ({results['passed']}/{results['total']})"
    else:
        results["summary"] = f"❌ All tests failed (0/{results['total']})"

    return results


def _format_notification(result: dict) -> str:
    """Format result as notification message."""
    lines = [
        f"**{result['summary']}**",
        "",
        "**Results:**",
    ]
    
    for detail in result["details"]:
        lines.append(f"• {detail}")
    
    lines.append("")
    
    if result["success"]:
        lines.extend([
            "**✅ Next Steps:**",
            "Your inverter is responding correctly!",
            "You can now install the integration.",
        ])
    elif result["passed"] > 0:
        lines.extend([
            "**⚠️ Troubleshooting:**",
            "Some registers failed. Try:",
            "• Test during daytime (inverter on)",
            "• Check if correct model selected",
            "• Wait for inverter to fully boot",
        ])
    else:
        lines.extend([
            "**❌ Troubleshooting:**",
            "No registers responded. Check:",
            "• Wiring (try swapping A/B)",
            "• Slave ID (try 1, 2, or 3)",
            "• Inverter is powered on",
            "• Baud rate is 9600",
        ])
    
    return "\n".join(lines)