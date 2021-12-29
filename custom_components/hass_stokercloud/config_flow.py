import voluptuous as vol
from .const import DOMAIN
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME
import homeassistant.helpers.config_validation as cv

DATA_SCHEMA = vol.Schema({vol.Required(CONF_USERNAME): cv.string})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, info):
        if info is not None:
            pass  # TODO: process info

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA
        )