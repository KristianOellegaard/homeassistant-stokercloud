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

import logging


logger = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(minutes=1)

async def async_setup_entry(hass, config, async_add_entities):
    """Set up the sensor platform."""
    client = hass.data[DOMAIN][config.entry_id]
    serial = client.controller_data().serial_number  # Avoid multi fetch
    async_add_entities([
        StokerCloudControllerBinarySensor(client, serial, 'Running', 'running', 'power'),
        StokerCloudControllerBinarySensor(client, serial, 'Alarm', 'alarm', 'problem'),
        StokerCloudControllerSensor(client, serial, 'Boiler Temperature', 'boiler_temperature', 'temperature'),
        StokerCloudControllerSensor(client, serial, 'Boiler Effect', 'boiler_kwh', 'power'),
    ])


class StokerCloudControllerMixin:
    def __init__(self, client: StokerCloudClient, serial, name: str, client_key: str):
        """Initialize the sensor."""
        logging.debug("Initializing sensor %s" % name)
        self._state = None
        self._name = name
        self.client = client
        self.client_key = client_key
        self._serial = serial
        self.controller_data = None

    @property
    def unique_id(self):
        """The unique id of the sensor."""
        return f'{self.serial}-{self._name}'

    @property
    def device_class(self):
        return self._device_class

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._state is PowerState.ON

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        logger.debug("Updating %s" % self.name)
        self.controller_data = self.client.controller_data()
        self._state = getattr(self.controller_data, self.client_key)


class StokerCloudControllerBinarySensor(StokerCloudControllerMixin, BinarySensorEntity):
    """Representation of a Sensor."""

    def __init__(self, client: StokerCloudClient, serial, name: str, client_key: str, device_class):
        """Initialize the sensor."""
        super(StokerCloudControllerBinarySensor, self).__init__(client, serial, name, client_key)
        self._device_class = device_class

    @property
    def is_on(self):
        """If the switch is currently on or off."""
        return self._state is PowerState.ON




class StokerCloudControllerSensor(StokerCloudControllerMixin, BinarySensorEntity):
    """Representation of a Sensor."""

    def __init__(self, client: StokerCloudClient, serial, name: str, client_key: str, device_class):
        """Initialize the sensor."""
        super(StokerCloudControllerSensor, self).__init__(client, serial, name, client_key)
        self._device_class = device_class