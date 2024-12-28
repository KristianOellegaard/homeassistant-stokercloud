"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


from stokercloud.controller_data import PowerState, Unit, Value
from stokercloud.client import Client as StokerCloudClient


import datetime
from homeassistant.const import CONF_USERNAME, UnitOfPower, UnitOfTemperature, UnitOfMass
from .const import DOMAIN
from .mixins import StokerCloudControllerMixin

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
        StokerCloudControllerSensor(client, serial, 'Boiler Temperature', 'boiler_temperature_current', SensorDeviceClass.TEMPERATURE),
        StokerCloudControllerSensor(client, serial, 'Boiler Temperature Requested', 'boiler_temperature_requested', SensorDeviceClass.TEMPERATURE),
        StokerCloudControllerSensor(client, serial, 'Boiler Effect', 'boiler_kwh', SensorDeviceClass.POWER),
        StokerCloudControllerSensor(client, serial, 'Total Consumption', 'consumption_total', state_class=SensorStateClass.TOTAL_INCREASING), # state class STATE_CLASS_TOTAL_INCREASING
        StokerCloudControllerSensor(client, serial, 'State', 'state'),

        StokerCloudWaterHeaterTemperatureSensor(client, serial, 'Current Water Heater Temperature', 'hotwater_temperature_current'),
        StokerCloudWaterHeaterTemperatureSensor(client, serial, 'Requested Water Heater Temperature', 'hotwater_temperature_requested'),
    ])




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

    @property
    def device_class(self):
        return self._device_class


class StokerCloudControllerSensor(StokerCloudControllerMixin, SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, client: StokerCloudClient, serial, name: str, client_key: str, device_class=None, state_class=None):
        """Initialize the sensor."""
        super(StokerCloudControllerSensor, self).__init__(client, serial, name, client_key)
        self._device_class = device_class
        self._attr_state_class = state_class

    @property
    def device_class(self):
        return self._device_class

    @property
    def native_value(self):
        """Return the value reported by the sensor."""
        if self._state:
            if isinstance(self._state, Value):
                return self._state.value
            return self._state

    @property
    def native_unit_of_measurement(self):
        if self._state and isinstance(self._state, Value):
            return {
                Unit.KWH: UnitOfPower.WATT,
                Unit.DEGREE: UnitOfTemperature.CELSIUS,
                Unit.KILO_GRAM: UnitOfMass.KILOGRAMS,
            }.get(self._state.unit)

class StokerCloudWaterHeaterTemperatureSensor(StokerCloudControllerMixin, SensorEntity):
    """Representation of a Water Heater Temperature Sensor."""

    def __init__(self, client, serial, name, client_key):
        """Initialize the water heater temperature sensor."""
        super().__init__(client, serial, name, client_key)
        self._name = name
        self._client_key = client_key

    @property
    def native_value(self):
        """Return the value reported by the water heater temperature sensor with 2 decimal places."""
        if self._state:
            if hasattr(self._state, 'value'):
                return round(self._state.value, 2)  # Round to 2 decimal places
            return round(self._state, 2)

    @property
    def device_class(self):
        """Return the device class for temperature."""
        return SensorDeviceClass.TEMPERATURE

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement (Celsius)."""
        return UnitOfTemperature.CELSIUS

    @property
    def available(self):
        """Return if the sensor is available (state is not None)."""
        return self._state is not None