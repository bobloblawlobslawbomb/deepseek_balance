"""Constants for Deepseek Balance.
"""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "deepseek_balance"

CONF_API_KEY: Final = "api_key"
CONF_UPDATE_INTERVAL: Final = "update_interval"

DEFAULT_UPDATE_INTERVAL: Final = 300
MIN_UPDATE_INTERVAL: Final = 60
MAX_UPDATE_INTERVAL: Final = 86400

API_BASE_URL: Final = "https://api.deepseek.com"
API_TIMEOUT: Final = 30

ATTR_CURRENCY: Final = "currency"
ATTR_GRANTED_BALANCE: Final = "granted_balance"
ATTR_TOPPED_UP_BALANCE: Final = "topped_up_balance"
