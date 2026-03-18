from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

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
            },
            extra=vol.ALLOW_EXTRA,
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                # hassfest disallows hardcoded URLs in translated strings, so we inject them here.
                "open_data_url": "https://www.saihebro.com/datos/opendata",
                "registration_url": "https://www.saihebro.com/usuarios/registro",
            },
        )

    async def async_step_scope(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}
        catalog = get_signals_catalog(self.hass)
        scopes = catalog.get_scopes()

        if user_input is not None:
            # We validate/display scope using localized labels.
            # `cv.multi_select()` returns a list, but we enforce selecting exactly one item.
            scope_list: list[str] = user_input[CONF_SCOPE]
            self._data[CONF_SCOPE] = scope_list[0]
            return await self.async_step_zone()

        # Localize the *label* shown in the UI for scope options.
        # The underlying value (used by the catalog/filtering) stays the same.
        lang = (self.hass.config.language or "").lower()
        is_english = lang.startswith("en")
        if is_english:
            scope_labels = {
                "Río": "River",
                "Embalse": "Reservoir",
                "Canal": "Canal",
                "Meteorología": "Meteorology",
            }
        else:
            # Spanish (and default fallback) keeps the existing catalog values.
            scope_labels = {
                "Río": "Río",
                "Embalse": "Embalse",
                "Canal": "Canal",
                "Meteorología": "Meteorología",
            }

        scope_choices = {s: scope_labels.get(s, s) for s in scopes}

        data_schema = vol.Schema(
            {
                vol.Required(CONF_SCOPE): vol.All(
                    cv.multi_select(scope_choices),
                    # enforce "single choice" while still showing localized labels
                    vol.Length(min=1, max=1),
                ),
            },
            extra=vol.ALLOW_EXTRA,
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
            },
            extra=vol.ALLOW_EXTRA,
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
        station_choices = {s["id"]: f'{s["id"]} – {s["name"]}' for s in stations}

        if user_input is not None:
            station_ids: list[str] = user_input.get(CONF_STATION_IDS, [])
            if not station_ids:
                errors[CONF_STATION_IDS] = "station_required"
            elif len(station_ids) > 5:
                errors[CONF_STATION_IDS] = "too_many_stations"
            else:
                self._data[CONF_STATION_IDS] = station_ids
                return await self.async_step_categories()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_STATION_IDS): cv.multi_select(station_choices),
            },
            extra=vol.ALLOW_EXTRA,
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
        category_choices = {c: c for c in categories}

        if user_input is not None:
            categories_selected: list[str] = user_input.get(CONF_CATEGORIES, [])
            if not categories_selected:
                errors[CONF_CATEGORIES] = "category_required"
            else:
                self._data[CONF_CATEGORIES] = categories_selected
                return await self.async_step_signals()

        data_schema = vol.Schema(
            {
                vol.Required(CONF_CATEGORIES): cv.multi_select(category_choices)
            },
            extra=vol.ALLOW_EXTRA,
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
                vol.Optional(CONF_SIGNAL_IDS): cv.multi_select(signal_choices),
            },
            extra=vol.ALLOW_EXTRA,
        )
        return self.async_show_form(
            step_id="signals",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "signals_count": str(len(signal_choices)),
            },
        )
