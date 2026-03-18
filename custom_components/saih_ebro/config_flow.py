from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_CATEGORIES,
    CONF_SCOPE,
    CONF_SIGNAL_IDS,
    CONF_STATION_IDS,
    CONF_ZONE,
    DOMAIN,
)
from .signals_catalog import get_signals_catalog


class SaihEbroConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            api_key = user_input[CONF_API_KEY]
            self._data: dict[str, Any] = {CONF_API_KEY: api_key}
            return await self.async_step_scope()

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

    async def async_step_scope(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        catalog = get_signals_catalog(self.hass)
        scopes = catalog.get_scopes()

        if user_input is not None:
            scope = user_input[CONF_SCOPE]
            self._data[CONF_SCOPE] = scope
            return await self.async_step_zone()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_SCOPE): vol.In(scopes),
            }
        )
        return self.async_show_form(
            step_id="scope",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_zone(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        catalog = get_signals_catalog(self.hass)
        zones = catalog.get_zones_for_scope(self._data[CONF_SCOPE])

        if user_input is not None:
            zone = user_input[CONF_ZONE]
            self._data[CONF_ZONE] = zone
            return await self.async_step_stations()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ZONE): vol.In(zones),
            }
        )
        return self.async_show_form(
            step_id="zone",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_stations(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        catalog = get_signals_catalog(self.hass)
        stations = catalog.get_stations(
            scope=self._data[CONF_SCOPE],
            zone=self._data[CONF_ZONE],
        )
        station_choices = {
            s["id"]: f'{s["id"]} – {s["name"]}' for s in stations
        }

        if user_input is not None:
            station_ids: list[str] = user_input.get(CONF_STATION_IDS, [])
            if not station_ids:
                errors[CONF_STATION_IDS] = "station_required"
            else:
                self._data[CONF_STATION_IDS] = station_ids
                return await self.async_step_categories()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_STATION_IDS): vol.All(
                    [vol.In(list(station_choices.keys()))],
                    vol.Length(min=1, max=5),
                ),
            }
        )
        return self.async_show_form(
            step_id="stations",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_categories(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        catalog = get_signals_catalog(self.hass)
        categories = catalog.get_categories_for_stations(
            self._data[CONF_STATION_IDS]
        )

        if user_input is not None:
            categories_selected: list[str] = user_input.get(CONF_CATEGORIES, [])
            if not categories_selected:
                errors[CONF_CATEGORIES] = "category_required"
            else:
                self._data[CONF_CATEGORIES] = categories_selected
                return await self.async_step_signals()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_CATEGORIES): vol.All(
                    [vol.In(categories)],
                    vol.Length(min=1),
                )
            }
        )
        return self.async_show_form(
            step_id="categories",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_signals(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        catalog = get_signals_catalog(self.hass)
        candidates = catalog.get_signals(
            scope=self._data[CONF_SCOPE],
            zone=self._data[CONF_ZONE],
            station_ids=self._data[CONF_STATION_IDS],
            categories=self._data[CONF_CATEGORIES],
        )
        signal_choices = {s.id: s.name for s in candidates}

        if user_input is not None:
            signal_ids: list[str] = user_input.get(CONF_SIGNAL_IDS, [])
            if len(signal_ids) > 50:
                errors[CONF_SIGNAL_IDS] = "too_many_signals"
            else:
                self._data[CONF_SIGNAL_IDS] = signal_ids
                return self.async_create_entry(
                    title="SAIH Ebro",
                    data=self._data,
                )

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_SIGNAL_IDS): vol.All(
                    [vol.In(list(signal_choices.keys()))],
                    vol.Length(max=50),
                ),
            }
        )
        return self.async_show_form(
            step_id="signals",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "signals_count": str(len(signal_choices)),
            },
        )
