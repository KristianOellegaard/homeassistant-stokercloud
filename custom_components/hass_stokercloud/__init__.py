"""
NBE Stoker Cloud
"""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, PLATFORMS
from homeassistant.config_entries import ConfigEntry


def setup(hass: HomeAssistant, config: ConfigType) -> bool:

    for platform in PLATFORMS:
        hass.helpers.discovery.load_platform(platform, DOMAIN, {}, config)

    return True
