from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import SaihEbroCoordinator
from .const import DOMAIN
from .signals_catalog import get_signals_catalog


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: SaihEbroCoordinator = hass.data[DOMAIN][entry.entry_id]
    entry_id = entry.entry_id
    entry_title = entry.title

    catalog = get_signals_catalog(hass)

    entities: list[SaihEbroSensor] = []
    for signal_id in coordinator.signals:
        meta = catalog.get_signal(signal_id)
        if meta is None:
            continue
        entities.append(
            SaihEbroSensor(
                coordinator=coordinator,
                entry_id=entry_id,
                entry_title=entry_title,
                signal_id=signal_id,
                name=meta.name,
                unit=meta.unit,
                device_class=meta.device_class,
            )
        )

    async_add_entities(entities)


class SaihEbroSensor(CoordinatorEntity[SaihEbroCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SaihEbroCoordinator,
        entry_id: str,
        entry_title: str,
        signal_id: str,
        name: str | None,
        unit: str | None,
        device_class: str | None,
    ) -> None:
        super().__init__(coordinator)
        self._signal_id = signal_id
        self._attr_name = name
        self._attr_unique_id = f"saih_ebro_{entry_id}_{signal_id.lower()}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name=entry_title or "SAIH Ebro",
            manufacturer="SAIH Ebro / Confederación Hidrográfica del Ebro",
            configuration_url="https://www.saihebro.com/homepage/estado-cuenca-ebro",
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        item = self.coordinator.data.get(self._signal_id, {})
        return {
            "signal": self._signal_id,
            "description": item.get("descripcion"),
            "raw_unit": item.get("unidades"),
            "timestamp": item.get("fecha"),
            "trend": item.get("tendencia"),
            ATTR_ATTRIBUTION: "Datos proporcionados por SAIH Ebro – Confederación Hidrográfica del Ebro (CHE)",
        }

    @property
    def native_value(self) -> float | None:
        item = self.coordinator.data.get(self._signal_id)
        if not item:
            return None
        value = item.get("valor")
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @property
    def available(self) -> bool:
        return self._signal_id in self.coordinator.data

