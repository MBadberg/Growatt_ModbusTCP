"""Config flow for Growatt Modbus Integration."""
import logging
import voluptuous as vol
from typing import Any

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_SLAVE_ID,
    CONF_INVERTER_SERIES,
    DEFAULT_PORT,
    DEFAULT_SLAVE_ID,
)
from .device_profiles import get_available_profiles, get_profile

_LOGGER = logging.getLogger(__name__)


class GrowattModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Growatt Modbus."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user step."""
        errors = {}

        if user_input is not None:
            # Add register map based on series
            series = user_input.get(CONF_INVERTER_SERIES, "min_7000_10000_tl_x")
            profile = get_profile(series)
            user_input["register_map"] = profile["register_map"]
            
            # Set unique ID
            await self.async_set_unique_id(f"{user_input[CONF_HOST]}_{user_input[CONF_SLAVE_ID]}")
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        schema = vol.Schema({
            vol.Required(CONF_NAME, default="Growatt"): str,
            vol.Required(CONF_INVERTER_SERIES, default="min_7000_10000_tl_x"): vol.In(get_available_profiles()),
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
            vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get options flow."""
        return GrowattModbusOptionsFlow(config_entry)


class GrowattModbusOptionsFlow(config_entries.OptionsFlow):
    """Handle options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage options."""
        if user_input is not None:
            new_options = {
                "scan_interval": user_input.get("scan_interval", 30),
                "timeout": user_input.get("timeout", 10),
                "invert_grid_power": user_input.get("invert_grid_power", False),
            }
            
            if user_input.get("device_name") != self.config_entry.data.get(CONF_NAME):
                new_data = dict(self.config_entry.data)
                new_data[CONF_NAME] = user_input["device_name"]
                
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data=new_data,
                    options=new_options,
                    title=user_input["device_name"],
                )
            else:
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    options=new_options,
                )
            
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            return self.async_create_entry(title="", data=new_options)

        current_name = self.config_entry.data.get(CONF_NAME, "Growatt")
        current_scan_interval = self.config_entry.options.get("scan_interval", 30)
        current_timeout = self.config_entry.options.get("timeout", 10)
        current_invert = self.config_entry.options.get("invert_grid_power", False)

        schema = vol.Schema({
            vol.Required("device_name", default=current_name): cv.string,
            vol.Required("scan_interval", default=current_scan_interval): vol.All(
                vol.Coerce(int), vol.Range(min=5, max=300)
            ),
            vol.Required("timeout", default=current_timeout): vol.All(
                vol.Coerce(int), vol.Range(min=1, max=60)
            ),
            vol.Required("invert_grid_power", default=current_invert): bool,
        })

        return self.async_show_form(step_id="init", data_schema=schema)