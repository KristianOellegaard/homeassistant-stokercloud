"""
NBE Stoker Cloud
"""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, PLATFORMS

def setup(hass: HomeAssistant, config: ConfigType) -> bool:

    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True