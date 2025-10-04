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
    CONF_CONNECTION_TYPE,
    CONF_DEVICE_PATH,
    CONF_BAUDRATE,
    CONF_REGISTER_MAP,
    REGISTER_MAPS,
    DEFAULT_PORT,
    DEFAULT_SLAVE_ID,
    DEFAULT_BAUDRATE,
)
from .coordinator import test_connection

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME, default="Growatt Inverter"): str,
    vol.Required(CONF_CONNECTION_TYPE, default="tcp"): vol.In(["tcp", "serial"]),
})

STEP_TCP_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
    vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
    vol.Required(CONF_REGISTER_MAP, default="MIN_10000_TL_X_OFFICIAL"): vol.In(list(REGISTER_MAPS.keys())),  # ← Changed here
})

STEP_SERIAL_DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_PATH, default="/dev/ttyUSB0"): str,
    vol.Required(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): int,
    vol.Required(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): int,
    vol.Required(CONF_REGISTER_MAP, default="MIN_10000_TL_X_OFFICIAL"): vol.In(list(REGISTER_MAPS.keys())),  # ← Changed here
})


class GrowattModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Growatt Modbus."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.config_data = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Store the basic configuration
            self.config_data.update(user_input)
            
            # Proceed to connection-specific configuration
            if user_input[CONF_CONNECTION_TYPE] == "tcp":
                return await self.async_step_tcp()
            else:
                return await self.async_step_serial()

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "tcp_description": "Connect via Ethernet/WiFi adapter (EW11, USR-W630, etc.)",
                "serial_description": "Connect via USB-to-RS485 adapter"
            }
        )

    async def async_step_tcp(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle TCP connection configuration."""
        errors = {}

        if user_input is not None:
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

        return self.async_show_form(
            step_id="tcp",
            data_schema=STEP_TCP_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "register_maps": ", ".join(f"{k}: {v['name']}" for k, v in REGISTER_MAPS.items())
            }
        )

    async def async_step_serial(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle serial connection configuration."""
        errors = {}

        if user_input is not None:
            # Test the connection
            self.config_data.update(user_input)
            
            try:
                # Test connection in executor to avoid blocking
                result = await self.hass.async_add_executor_job(
                    test_connection, self.config_data
                )
                
                if result["success"]:
                    # Connection successful, create the entry
                    await self.async_set_unique_id(f"{user_input[CONF_DEVICE_PATH]}_{user_input[CONF_SLAVE_ID]}")
                    self._abort_if_unique_id_configured()
                    
                    return self.async_create_entry(
                        title=self.config_data[CONF_NAME],
                        data=self.config_data,
                        description=f"Connected to {user_input[CONF_DEVICE_PATH]} @ {user_input[CONF_BAUDRATE]} baud (Slave {user_input[CONF_SLAVE_ID]})"
                    )
                else:
                    errors["base"] = "cannot_connect"
                    _LOGGER.error("Connection test failed: %s", result.get("error", "Unknown error"))
                    
            except Exception as err:
                _LOGGER.exception("Unexpected error during connection test")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="serial",
            data_schema=STEP_SERIAL_DATA_SCHEMA,
            errors=errors,
            description_placeholders={
                "register_maps": ", ".join(f"{k}: {v['name']}" for k, v in REGISTER_MAPS.items())
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
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Required(
                "scan_interval",
                default=self.config_entry.options.get("scan_interval", 30)
            ): vol.All(vol.Coerce(int), vol.Range(min=5, max=300)),
            vol.Required(
                "timeout",
                default=self.config_entry.options.get("timeout", 10)
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=60)),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            description_placeholders={
                "scan_interval_description": "How often to poll the inverter (seconds)",
                "timeout_description": "Connection timeout (seconds)"
            }
        )