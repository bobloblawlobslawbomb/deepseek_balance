"""Sensor platform for Deepseek Balance.

Generated with ha-integration@aurora-smart-home v1.0.0
https://github.com/tonylofgren/aurora-smart-home
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTR_CURRENCY, ATTR_GRANTED_BALANCE, ATTR_TOPPED_UP_BALANCE
from .coordinator import DeepseekBalanceCoordinator


@dataclass(frozen=True, kw_only=True)
class DeepseekBalanceSensorEntityDescription(SensorEntityDescription):
    """Describes a Deepseek balance sensor entity."""

    value_fn: Callable[[dict], StateType]
    currency_fn: Callable[[dict], str]
    extra_attrs_fn: Callable[[dict], dict[str, str]] | None = None


def _build_sensor_descriptions(
    balance_infos: list[dict],
) -> tuple[DeepseekBalanceSensorEntityDescription, ...]:
    """Build sensor descriptions from the balance infos in coordinator data."""
    descriptions: list[DeepseekBalanceSensorEntityDescription] = []

    for info in balance_infos:
        currency = info.get("currency", "USD")

        descriptions.append(
            DeepseekBalanceSensorEntityDescription(
                key=f"{currency}_total_balance",
                translation_key="total_balance",
                device_class=SensorDeviceClass.MONETARY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=currency,
                value_fn=lambda d, c=currency: _get_balance(d, c, "total_balance"),
                currency_fn=lambda d, c=currency: c,
                extra_attrs_fn=lambda d, c=currency: _get_extra_attrs(d, c),
            )
        )
        descriptions.append(
            DeepseekBalanceSensorEntityDescription(
                key=f"{currency}_granted_balance",
                translation_key="granted_balance",
                device_class=SensorDeviceClass.MONETARY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=currency,
                value_fn=lambda d, c=currency: _get_balance(d, c, "granted_balance"),
                currency_fn=lambda d, c=currency: c,
                extra_attrs_fn=lambda d, c=currency: _get_extra_attrs(d, c),
            )
        )
        descriptions.append(
            DeepseekBalanceSensorEntityDescription(
                key=f"{currency}_topped_up_balance",
                translation_key="topped_up_balance",
                device_class=SensorDeviceClass.MONETARY,
                state_class=SensorStateClass.MEASUREMENT,
                native_unit_of_measurement=currency,
                value_fn=lambda d, c=currency: _get_balance(d, c, "topped_up_balance"),
                currency_fn=lambda d, c=currency: c,
                extra_attrs_fn=lambda d, c=currency: _get_extra_attrs(d, c),
            )
        )

    return tuple(descriptions)


def _get_balance(data: dict, currency: str, field: str) -> float | None:
    """Extract a balance field for a given currency."""
    for info in data.get("balance_infos", []):
        if info.get("currency") == currency:
            try:
                return float(info.get(field, 0))
            except (ValueError, TypeError):
                return None
    return None


def _get_extra_attrs(data: dict, currency: str) -> dict[str, str]:
    """Build extra attributes for a given currency."""
    for info in data.get("balance_infos", []):
        if info.get("currency") == currency:
            return {
                ATTR_CURRENCY: info.get("currency", ""),
                ATTR_GRANTED_BALANCE: info.get("granted_balance", "0.00"),
                ATTR_TOPPED_UP_BALANCE: info.get("topped_up_balance", "0.00"),
            }
    return {}


class DeepseekBalanceSensor(CoordinatorEntity[DeepseekBalanceCoordinator], SensorEntity):
    """Sensor showing a Deepseek account balance."""

    entity_description: DeepseekBalanceSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DeepseekBalanceCoordinator,
        entry: ConfigEntry,
        description: DeepseekBalanceSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = coordinator.device_info

    @property
    def native_value(self) -> StateType:
        """Return the balance value."""
        return self.entity_description.value_fn(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, str] | None:
        """Return extra state attributes."""
        if self.entity_description.extra_attrs_fn:
            return self.entity_description.extra_attrs_fn(self.coordinator.data)
        return None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Deepseek Balance sensors from a config entry."""
    coordinator: DeepseekBalanceCoordinator = entry.runtime_data

    entities: list[DeepseekBalanceSensor] = []
    for description in _build_sensor_descriptions(
        coordinator.data.get("balance_infos", [])
    ):
        entities.append(DeepseekBalanceSensor(coordinator, entry, description))

    async_add_entities(entities)
