"""Config flow for Growatt Modbus Integration."""
import logging
import voluptuous as vol
from typing import Any

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_SLAVE_ID,
    CONF_REGISTER_MAP,
    CONF_INVERTER_SERIES,
    CONF_INVERT_GRID_POWER,
    DEFAULT_PORT,
    DEFAULT_SLAVE_ID,
)
from .coordinator import test_connection
from .device_profiles import get_available_profiles, get_profile

_LOGGER = logging.getLogger(__name__)


class GrowattModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Growatt Modbus."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.config_data = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step - inverter series selection."""
        errors = {}

        if user_input is not None:
            # Store the basic configuration
            self.config_data.update(user_input)
            
            # Proceed to TCP configuration
            return await self.async_step_tcp()

        user_schema = vol.Schema({
            vol.Required(CONF_NAME, default="Growatt"): str,
            vol.Required(CONF_INVERTER_SERIES, default="min_7000_10000_tl_x"): vol.In(get_available_profiles()),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=user_schema,
            errors=errors,
        )

    async def async_step_tcp(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle TCP connection configuration."""
        errors = {}

        if user_input is not None:
            # Get the profile to set the correct register map
            series = self.config_data.get(CONF_INVERTER_SERIES, "min_7000_10000_tl_x")
            profile = get_profile(series)
            
            # Add register map from profile
            user_input[CONF_REGISTER_MAP] = profile.register_map if profile else "MIN_7000_10000TL_X"
            
            # Test the connection
            self.config_data.update(user_input)
            
            try:
                # Test connection in executor to avoid blocking
                result = await self.hass.async_add_executor_job(
                    test_connection, self.config_data
                )
                
                if result["success"]:
                    # Connection successful, create the entry
                    await self.async_set_unique_id(f"{user_input[CONF_HOST]}_{user_input[CONF_SLAVE_ID]}")
                    self._abort_if_unique_id_configured()
                    
                    return self.async_create_entry(
                        title=self.config_data[CONF_NAME],
                        data=self.config_data,
                        description=f"Connected to {user_input[CONF_HOST]}:{user_input[CONF_PORT]} (Slave {user_input[CONF_SLAVE_ID]})"
                    )
                else:
                    errors["base"] = "cannot_connect"
                    _LOGGER.error("Connection test failed: %s", result.get("error", "Unknown error"))
                    
            except Exception as err:
                _LOGGER.exception("Unexpected error during connection test")
                errors["base"] = "unknown"

        # Get series info for description
        series = self.config_data.get(CONF_INVERTER_SERIES, "min_7000_10000_tl_x")
        profile = get_profile(series)
        series_info = f"{profile.name} - {profile.description}" if profile else "Unknown series"

        tcp_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
            vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
        })

        return self.async_show_form(
            step_id="tcp",
            data_schema=tcp_schema,
            errors=errors,
            description_placeholders={
                "series_info": series_info,
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Create the options flow."""
        return GrowattModbusOptionsFlow(config_entry)


class GrowattModbusOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Growatt Modbus."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors = {}

        if user_input is not None:
            # Update options
            new_options = {
                "scan_interval": user_input.get("scan_interval", 30),
                "timeout": user_input.get("timeout", 10),
                "invert_grid_power": user_input.get("invert_grid_power", False),
            }
            
            # Check if device name changed - this needs to update config data, not options
            if user_input.get("device_name") != self.config_entry.data.get(CONF_NAME):
                # Update the config entry data with new device name
                new_data = dict(self.config_entry.data)
                new_data[CONF_NAME] = user_input["device_name"]
                
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data=new_data,
                    options=new_options,
                    title=user_input["device_name"],
                )
            else:
                # Just update options
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    options=new_options,
                )
            
            # Reload the integration to apply changes
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            
            return self.async_create_entry(title="", data=new_options)

        # Build the options schema with current values
        current_name = self.config_entry.data.get(CONF_NAME, "Growatt")
        current_scan_interval = self.config_entry.options.get("scan_interval", 30)
        current_timeout = self.config_entry.options.get("timeout", 10)
        current_invert = self.config_entry.options.get("invert_grid_power", False)

        options_schema = vol.Schema({
            vol.Required(
                "device_name",
                default=current_name
            ): cv.string,
            vol.Required(
                "scan_interval",
                default=current_scan_interval
            ): vol.All(vol.Coerce(int), vol.Range(min=5, max=300)),
            vol.Required(
                "timeout",
                default=current_timeout
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
            vol.Required(
                "invert_grid_power",
                default=current_invert
            ): bool,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors,
            description_placeholders={
                "device_name_description": "Friendly name for the device (appears before all sensor names)",
                "scan_interval_description": "How often to poll the inverter (seconds)",
                "timeout_description": "Connection timeout (seconds)",
                "invert_grid_power_description": "Reverse grid power sign (enable if CT clamp installed backwards - import/export swapped)"
            }
        )