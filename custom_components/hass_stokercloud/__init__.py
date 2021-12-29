"""
NBE Stoker Cloud
"""

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, PLATFORMS

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)