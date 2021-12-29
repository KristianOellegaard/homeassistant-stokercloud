import voluptuous as vol
from .const import DOMAIN, DATA_SCHEMA
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                username = user_input[CONF_USERNAME]
                info = f"Stoker Cloud {username}"
                return self.async_create_entry(title=info, data=user_input)
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )