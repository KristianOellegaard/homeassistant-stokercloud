"""
NBE Stoker Cloud
"""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN, PLATFORMS
from homeassistant.config_entries import ConfigEntry


def setup(hass: HomeAssistant, config: ConfigType) -> bool:

    hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True