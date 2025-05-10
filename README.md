# homeassistant-stokercloud

This is an integration between Home Assistant and stokercloud.dk

# Install

You can install the plugin via HACS using the following steps.

[![image](https://github.com/user-attachments/assets/e99278d9-5121-40a4-b9c7-af48561a9140)](https://my.home-assistant.io/redirect/hacs_repository/?owner=nagels&repository=homeassistant-stokercloud&category=integration)

Manual Install:
1. Open HACS
2. Click the three dots on the top right
4. Click "Custom repositories"
5. Add https://github.com/KristianOellegaard/homeassistant-stokercloud and a category of your choice (integration will work just fine)

# Adding the integration

Go to **Settings -> Devices & services**

![image](https://github.com/user-attachments/assets/c2137e41-156d-4814-829a-ac763e08d873)

**+ ADD INTEGRATION** (Can be found in the bottom right corner)

![image](https://github.com/user-attachments/assets/e99278d9-5121-40a4-b9c7-af48561a9140)

Search for **NBE**

![image](https://github.com/user-attachments/assets/f2424009-c2bf-480a-adcd-1ad48b1c67f8)

Insert your Stokercloud username (This can be found in your stokercloud URL. https://stokercloud.dk/v3/#/USERNAME/main-page)

![image](https://github.com/user-attachments/assets/1cc6e285-b653-436b-9396-ed3c3a47f0d4)

Currently the integration is read-only so you do not need to enter your password

If the entities added are "Unknown" - Please give the integration a few minutes to fetch the data.
An alternative to waiting is to restart HA.
