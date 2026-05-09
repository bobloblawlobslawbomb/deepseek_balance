# Deepseek Balance

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/bobloblawlobslawbomb/deepseek_balance.svg)](https://github.com/bobloblawlobslawbomb/deepseek_balance/releases)

Monitor your Deepseek API account balance directly in Home Assistant. Shows your total,
granted, and topped-up balance across all currencies.

## Installation

### HACS (Recommended)
1. Open HACS → Integrations → Custom repositories
2. Add `https://github.com/bobloblawlobslawbomb/deepseek_balance` as Integration
3. Search and install "Deepseek Balance"
4. Restart Home Assistant

### Manual
1. Copy `custom_components/deepseek_balance` to your `custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings → Integrations
2. Click "+ Add Integration"
3. Search for "Deepseek Balance"
4. Enter your Deepseek API key (from the Deepseek dashboard)
5. Optionally adjust the update interval in the integration options

## Entities

| Entity | Type | Description |
|--------|------|-------------|
| API Available | Binary Sensor | Whether the Deepseek API is reachable |
| Total Balance | Sensor | Your total account balance |
| Granted Balance | Sensor | Amount granted via credits/promotions |
| Topped Up Balance | Sensor | Amount you've topped up |

All balance sensors use the MONETARY device class and are shown in their
respective currency (e.g., USD).

---

*Generated with [ha-integration@aurora-smart-home](https://github.com/tonylofgren/aurora-smart-home)*
