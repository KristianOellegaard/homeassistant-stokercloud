"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


from stokercloud.controller_data import PowerState, Unit
from stokercloud.client import Client as StokerCloudClient


import datetime
from homeassistant.const import CONF_USERNAME, POWER_KILO_WATT, TEMP_CELSIUS
from .const import DOMAIN

import logging


logger = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(minutes=1)

async def async_setup_entry(hass, config, async_add_entities):
    """Set up the sensor platform."""
    client = hass.data[DOMAIN][config.entry_id]
    serial = config.data[CONF_USERNAME]
    async_add_entities([
        StokerCloudControllerBinarySensor(client, serial, 'Running', 'running', 'power'),
        StokerCloudControllerBinarySensor(client, serial, 'Alarm', 'alarm', 'problem'),
        StokerCloudControllerSensor(client, serial, 'Boiler Temperature', 'boiler_temperature', SensorDeviceClass.TEMPERATURE),
        StokerCloudControllerSensor(client, serial, 'Boiler Effect', 'boiler_kwh', SensorDeviceClass.POWER),
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
        return f'{self._serial}-{self._name}'

    @property
    def device_class(self):
        return self._device_class

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "NBE %s" % self._name

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
        logger.debug("New state %s" % self._state)


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


class StokerCloudControllerSensor(StokerCloudControllerMixin, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, client: StokerCloudClient, serial, name: str, client_key: str, device_class):
        """Initialize the sensor."""
        super(StokerCloudControllerSensor, self).__init__(client, serial, name, client_key)
        self._device_class = device_class


    @property
    def native_value(self):
        """Return the value reported by the sensor."""
        if self._state:
            return self._state.value

    @property
    def native_unit_of_measurement(self):
        if self._state:
            return {
                Unit.KWH: POWER_KILO_WATT,
                Unit.DEGREE: TEMP_CELSIUS,
            }.get(self._state.unit)