from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_SIGNALS, DEFAULT_SIGNALS


class SaihEbroConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            api_key = user_input[CONF_API_KEY]
            signals = user_input.get(CONF_SIGNALS, "")

            return self.async_create_entry(
                title="SAIH Ebro",
                data={
                    CONF_API_KEY: api_key,
                    CONF_SIGNALS: signals,
                },
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Optional(
                    CONF_SIGNALS,
                    default=",".join(DEFAULT_SIGNALS),
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

