from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import SaihEbroCoordinator
from .const import DOMAIN, SENSORS_TORTOSA


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: SaihEbroCoordinator = hass.data[DOMAIN][entry.entry_id]
    entry_id = entry.entry_id

    entities: list[SaihEbroSensor] = []
    for signal_id in coordinator.signals:
        meta = SENSORS_TORTOSA.get(signal_id, {})
        entities.append(
            SaihEbroSensor(
                coordinator=coordinator,
                entry_id=entry_id,
                signal_id=signal_id,
                name=meta.get("name"),
                unit=meta.get("unit"),
                device_class=meta.get("device_class"),
            )
        )

    async_add_entities(entities)


class SaihEbroSensor(CoordinatorEntity[SaihEbroCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SaihEbroCoordinator,
        entry_id: str,
        signal_id: str,
        name: str | None,
        unit: str | None,
        device_class: str | None,
    ) -> None:
        super().__init__(coordinator)
        self._signal_id = signal_id
        self._attr_name = name
        # Incluir entry_id permite tener varias configuraciones (p.ej. varias estaciones)
        # sin colisión de unique_id entre sensores.
        self._attr_unique_id = f"saih_ebro_{entry_id}_{signal_id.lower()}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        item = self.coordinator.data.get(self._signal_id, {})
        return {
            "signal": self._signal_id,
            "description": item.get("descripcion"),
            "raw_unit": item.get("unidades"),
            "timestamp": item.get("fecha"),
            "trend": item.get("tendencia"),
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

