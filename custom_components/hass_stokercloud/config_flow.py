import voluptuous as vol
from .const import DOMAIN, DATA_SCHEMA
from homeassistant import config_entries



class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, info):
        if info is not None:
            pass  # TODO: process info

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA
        )