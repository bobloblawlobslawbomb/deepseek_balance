"""Binary sensor platform for Deepseek Balance.
"""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import DeepseekBalanceCoordinator

BINARY_SENSOR_DESCRIPTION = BinarySensorEntityDescription(
    key="is_available",
    translation_key="is_available",
    device_class=BinarySensorDeviceClass.CONNECTIVITY,
)


class DeepseekBalanceBinarySensor(
    CoordinatorEntity[DeepseekBalanceCoordinator], BinarySensorEntity
):
    """Binary sensor indicating whether the Deepseek API is available."""

    entity_description: BinarySensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DeepseekBalanceCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = BINARY_SENSOR_DESCRIPTION
        self._attr_unique_id = f"{entry.entry_id}_is_available"
        self._attr_device_info = coordinator.device_info

    @property
    def is_on(self) -> bool:
        """Return true if the API is available."""
        return bool(self.coordinator.data.get("is_available", False))


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Deepseek Balance binary sensor from a config entry."""
    coordinator: DeepseekBalanceCoordinator = entry.runtime_data
    async_add_entities([DeepseekBalanceBinarySensor(coordinator, entry)])
