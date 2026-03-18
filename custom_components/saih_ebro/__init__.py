from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any, Iterable

import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    API_BASE_URL,
    CONF_CATEGORIES,
    CONF_SCOPE,
    CONF_SIGNAL_IDS,
    CONF_STATION_IDS,
    CONF_ZONE,
    DOMAIN,
)
from .signals_catalog import get_signals_catalog

PLATFORMS: list[str] = ["sensor"]


class SaihEbroCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        signals: Iterable[str],
    ) -> None:
        self._api_key = api_key
        self._signals = list(signals)
        # SAIH Ebro actualmente presenta problemas de cadena de certificados
        # intermedios. Usamos verify_ssl=False solo para esta integración.
        self._session = async_get_clientsession(hass, verify_ssl=False)
        super().__init__(
            hass,
            logging.getLogger(__name__),
            name="SAIH Ebro",
            update_interval=timedelta(minutes=5),
        )

    @property
    def signals(self) -> list[str]:
        return self._signals

    async def _async_update_data(self) -> dict[str, Any]:
        params = {
            "senal": ",".join(self._signals),
            "inicio": "",
            "apikey": self._api_key,
        }
        try:
            async with async_timeout.timeout(30):
                async with self._session.get(API_BASE_URL, params=params) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(f"HTTP {resp.status}")
                    data = await resp.json()
        except Exception as err:  # type: ignore[no-untyped-except]
            raise UpdateFailed(f"Error fetching data: {err}") from err

        result: dict[str, Any] = {}
        if isinstance(data, list):
            for item in data:
                signal = item.get("senal")
                if signal:
                    result[signal] = item

        return result


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api_key: str = entry.data[CONF_API_KEY]

    catalog = get_signals_catalog(hass)
    scope: str = entry.data[CONF_SCOPE]
    zone: str = entry.data[CONF_ZONE]
    station_ids: list[str] = entry.data[CONF_STATION_IDS]
    categories: list[str] = entry.data[CONF_CATEGORIES]
    signal_ids: list[str] = entry.data.get(CONF_SIGNAL_IDS, [])

    if signal_ids:
        selected = catalog.get_signals_by_ids(signal_ids)
    else:
        selected = catalog.get_signals(
            scope=scope,
            zone=zone,
            station_ids=station_ids,
            categories=categories,
        )

    signals = [s.id for s in selected]

    coordinator = SaihEbroCoordinator(hass, api_key, signals)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok

