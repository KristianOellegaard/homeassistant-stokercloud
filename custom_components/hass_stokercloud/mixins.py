from stokercloud.client import Client as StokerCloudClient

import logging

logger = logging.getLogger(__name__)

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

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        logger.debug("Updating %s" % self.name)
        self.controller_data = self.client.controller_data()
        self._state = getattr(self.controller_data, self.client_key)
        logger.debug("New state %s" % self._state)