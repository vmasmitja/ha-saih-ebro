from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import homeassistant.util.json as json_util
from homeassistant.core import HomeAssistant

from .const import DOMAIN


@dataclass(frozen=True)
class SignalMeta:
    id: str
    name: str
    scope: str
    zone: str
    hydro_zone_id: str | None
    hydro_zone_name: str | None
    station_id: str
    station_name: str
    category: str
    unit: str | None
    device_class: str | None
    has_forecast: bool


class SignalsCatalog:
    def __init__(self, signals: list[SignalMeta]) -> None:
        self._signals: list[SignalMeta] = signals
        self._by_id: dict[str, SignalMeta] = {s.id: s for s in signals}

    # Official hydrological zones from SAIH maps (H1..H22 + HG "Toda la Cuenca").
    # We keep this list stable so the config wizard doesn't show "raw" zone strings
    # (like station local names or canal codes) for `scope == "Río"`.
    _HYDRO_ZONE_NAMES: list[str] = [
        "Alto Ebro (M.I.)",
        "Semi Alta (Miranda)",
        "Aragón-Irati",
        "Medio Ebro (M.I.)",
        "Gállego",
        "Bajo Cinca",
        "Segre",
        "Bajo Ebro",
        "Guadalope-Martín",
        "Bajo Jalón",
        "Semi Alta (Logroño)",
        "Arga",
        "Nogueras",
        "Alto Ebro (M.D.)",
        "Alto Aragón",
        "Alto Cinca",
        "Esera",
        "Huerva-Aguas Vivas",
        "Alto Jalón",
        "Medio Ebro (M.D.)",
        "Garona",
        "Toda la Cuenca",
    ]

    @property
    def signals(self) -> list[SignalMeta]:
        return self._signals

    def get_scopes(self) -> list[str]:
        return sorted({s.scope for s in self._signals})

    def get_zones_for_scope(self, scope: str) -> list[str]:
        if scope in {"Río", "Embalse"}:
            # Always present the same 22 official hydrological zones for the wizard.
            return list(self._HYDRO_ZONE_NAMES)

        return sorted({s.zone for s in self._signals if s.scope == scope})

    def get_stations(self, scope: str, zone: str) -> list[dict[str, Any]]:
        stations: dict[str, dict[str, Any]] = {}
        hydro_zone_mode = scope in {"Río", "Embalse"} and zone in self._HYDRO_ZONE_NAMES

        for sig in self._signals:
            if sig.scope != scope:
                continue

            if hydro_zone_mode:
                # Prefer the official hydrological zone naming; fall back to legacy `zone`
                # only when it already matches one of the official names.
                if not (sig.hydro_zone_name == zone or sig.zone == zone):
                    continue
            else:
                if sig.zone != zone:
                    continue

            if sig.station_id not in stations:
                stations[sig.station_id] = {
                    "id": sig.station_id,
                    "name": sig.station_name,
                    "scope": sig.scope,
                    "zone": sig.zone,
                }
        return sorted(stations.values(), key=lambda s: s["id"])

    def get_categories_for_stations(self, station_ids: list[str]) -> list[str]:
        station_set = set(station_ids)
        return sorted(
            {
                s.category
                for s in self._signals
                if s.station_id in station_set
            }
        )

    def get_signals(
        self,
        scope: str,
        zone: str,
        station_ids: list[str],
        categories: list[str],
    ) -> list[SignalMeta]:
        st_set = set(station_ids)
        cat_set = set(categories)
        hydro_zone_mode = scope in {"Río", "Embalse"} and zone in self._HYDRO_ZONE_NAMES
        return [
            s
            for s in self._signals
            if s.scope == scope
            and (
                (hydro_zone_mode and (s.hydro_zone_name == zone or s.zone == zone))
                or (not hydro_zone_mode and s.zone == zone)
            )
            and s.station_id in st_set
            and s.category in cat_set
        ]

    def get_signals_by_ids(self, signal_ids: list[str]) -> list[SignalMeta]:
        return [self._by_id[sid] for sid in signal_ids if sid in self._by_id]

    def get_signal(self, signal_id: str) -> SignalMeta | None:
        return self._by_id.get(signal_id)


def _load_signals_from_file(path: Path) -> list[SignalMeta]:
    data = json_util.load_json(path)
    signals: list[SignalMeta] = []
    for raw in data:
        signals.append(
            SignalMeta(
                id=raw["id"],
                name=raw.get("name", raw["id"]),
                scope=raw["scope"],
                zone=raw["zone"],
                hydro_zone_id=raw.get("hydro_zone_id"),
                hydro_zone_name=raw.get("hydro_zone_name"),
                station_id=raw["station_id"],
                station_name=raw.get("station_name", raw["station_id"]),
                category=raw["category"],
                unit=raw.get("unit"),
                device_class=raw.get("device_class"),
                has_forecast=bool(raw.get("has_forecast", False)),
            )
        )
    return signals


@lru_cache(maxsize=1)
def _build_catalog(base_path: Path) -> SignalsCatalog:
    signals_path = base_path / "signals.json"
    signals = _load_signals_from_file(signals_path)
    return SignalsCatalog(signals)


def get_signals_catalog(hass: HomeAssistant) -> SignalsCatalog:
    """Return a shared SignalsCatalog instance for this integration."""
    base_path = Path(hass.config.path()) / "custom_components" / DOMAIN
    return _build_catalog(base_path)

