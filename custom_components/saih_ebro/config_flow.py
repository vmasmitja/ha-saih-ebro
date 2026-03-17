from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import API_BASE_URL, DOMAIN


async def _validate_api_key(hass: HomeAssistant, api_key: str) -> None:
    """Realiza una llamada simple para validar que la API Key funciona."""
    params = {
        "senal": "A027C04TEMPA",
        "inicio": "",
        "apikey": api_key,
    }
    session = async_get_clientsession(hass)
    async with session.get(API_BASE_URL, params=params) as resp:
        if resp.status != 200:
            raise ValueError(f"HTTP {resp.status}")
        await resp.json()


class SaihEbroConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            api_key = user_input[CONF_API_KEY]
            try:
                await _validate_api_key(self.hass, api_key)
            except Exception:  # type: ignore[no-untyped-except]
                errors["base"] = "invalid_api_key"
            else:
                return self.async_create_entry(
                    title="SAIH Ebro",
                    data={CONF_API_KEY: api_key},
                )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

