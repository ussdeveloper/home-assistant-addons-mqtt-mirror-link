"""Config flow for MQTT Link."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MQTTLinkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for MQTT Link."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step - broker A configuration (local)."""
        errors = {}

        if user_input is not None:
            # Save broker A data and proceed to step 2
            self.broker_a_data = user_input
            return await self.async_step_broker_b()

        # Form for broker A
        data_schema = vol.Schema(
            {
                vol.Optional("broker_a_host", default="localhost"): str,
                vol.Optional("broker_a_port", default=1883): cv.port,
                vol.Optional("broker_a_username"): str,
                vol.Optional("broker_a_password"): str,
                vol.Optional("broker_a_topic", default="#"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "name": "Broker A (lokalny Home Assistant)"
            },
        )

    async def async_step_broker_b(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle broker B configuration (remote Home Assistant)."""
        errors = {}

        if user_input is not None:
            # Combine data from both steps
            config_data = {**self.broker_a_data, **user_input}
            
            # Create configuration entry
            return self.async_create_entry(
                title=f"MQTT Link: {config_data['broker_b_host']}",
                data=config_data,
            )

        # Form for broker B
        data_schema = vol.Schema(
            {
                vol.Required("broker_b_host"): str,
                vol.Optional("broker_b_port", default=1883): cv.port,
                vol.Optional("broker_b_username"): str,
                vol.Optional("broker_b_password"): str,
                vol.Optional("broker_b_topic", default="#"): str,
                vol.Optional("bidirectional", default=True): bool,
            }
        )

        return self.async_show_form(
            step_id="broker_b",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "name": "Broker B (zdalny Home Assistant)"
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return MQTTLinkOptionsFlow(config_entry)


class MQTTLinkOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for MQTT Link."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "broker_a_host",
                        default=self.config_entry.data.get("broker_a_host", "localhost"),
                    ): str,
                    vol.Optional(
                        "broker_a_port",
                        default=self.config_entry.data.get("broker_a_port", 1883),
                    ): cv.port,
                    vol.Optional(
                        "broker_a_username",
                        default=self.config_entry.data.get("broker_a_username", ""),
                    ): str,
                    vol.Optional(
                        "broker_a_password",
                        default=self.config_entry.data.get("broker_a_password", ""),
                    ): str,
                    vol.Optional(
                        "broker_a_topic",
                        default=self.config_entry.data.get("broker_a_topic", "#"),
                    ): str,
                    vol.Required(
                        "broker_b_host",
                        default=self.config_entry.data.get("broker_b_host"),
                    ): str,
                    vol.Optional(
                        "broker_b_port",
                        default=self.config_entry.data.get("broker_b_port", 1883),
                    ): cv.port,
                    vol.Optional(
                        "broker_b_username",
                        default=self.config_entry.data.get("broker_b_username", ""),
                    ): str,
                    vol.Optional(
                        "broker_b_password",
                        default=self.config_entry.data.get("broker_b_password", ""),
                    ): str,
                    vol.Optional(
                        "broker_b_topic",
                        default=self.config_entry.data.get("broker_b_topic", "#"),
                    ): str,
                    vol.Optional(
                        "bidirectional",
                        default=self.config_entry.data.get("bidirectional", True),
                    ): bool,
                }
            ),
        )
