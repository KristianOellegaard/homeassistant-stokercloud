"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


from stokercloud.controller_data import PowerState
from stokercloud.client import Client as StokerCloudClient


import datetime

from .const import DOMAIN

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(minutes=1)

async def async_setup_entry(hass, config, async_add_entities):
    """Set up the sensor platform."""
    client = hass.data[DOMAIN][config.entry_id]
    async_add_entities([
        StokerCloudControllerSensor(client, 'Running?', 'running', 'power'),
        StokerCloudControllerSensor(client, 'Alarm?', 'running', 'problem')
    ])


class StokerCloudControllerSensor(BinarySensorEntity):
    """Representation of a Sensor."""

    def __init__(self, client: StokerCloudClient, name: str, client_key: str, device_class):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self.client = client
        self.client_key = client_key
        self._device_class = device_class

        
    @property
    def device_class(self):
        return self._device_class

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._state is PowerState.ON

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = getattr(self.client.controller_data(), self.client_key)