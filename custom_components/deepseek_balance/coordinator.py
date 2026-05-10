"""Coordinator for Deepseek Balance.
"""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import TypedDict

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, API_TIMEOUT, DEFAULT_UPDATE_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class BalanceInfo(TypedDict):
    """Balance info for a single currency."""

    currency: str
    total_balance: str
    granted_balance: str
    topped_up_balance: str


class DeepseekData(TypedDict):
    """Data returned by the coordinator."""

    is_available: bool
    balance_infos: list[BalanceInfo]


class DeepseekBalanceCoordinator(DataUpdateCoordinator[DeepseekData]):
    """Coordinator for fetching Deepseek account balance."""

    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self._api_key = entry.data[CONF_API_KEY]
        self._session = async_get_clientsession(hass)

        update_interval = entry.options.get(
            "update_interval",
            entry.data.get("update_interval", DEFAULT_UPDATE_INTERVAL),
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
            config_entry=entry,
        )

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the Deepseek account."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.config_entry.entry_id)},
            name="Deepseek Account",
            manufacturer="Deepseek",
            entry_type="service",
        )

    async def _async_update_data(self) -> DeepseekData:
        """Fetch balance data from the Deepseek API."""
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }

        try:
            async with self._session.get(
                f"{API_BASE_URL}/user/balance",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT),
            ) as resp:
                if resp.status == 401:
                    raise ConfigEntryAuthFailed(
                        "Invalid API key. Please re-authenticate."
                    )
                resp.raise_for_status()
                data = await resp.json()
        except ConfigEntryAuthFailed:
            raise
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching balance data: {err}") from err

        balance_infos: list[BalanceInfo] = []
        for info in data.get("balance_infos", []):
            balance_infos.append(
                BalanceInfo(
                    currency=info.get("currency", "USD"),
                    total_balance=info.get("total_balance", "0.00"),
                    granted_balance=info.get("granted_balance", "0.00"),
                    topped_up_balance=info.get("topped_up_balance", "0.00"),
                )
            )

        return DeepseekData(
            is_available=data.get("is_available", False),
            balance_infos=balance_infos,
        )
