# Anker Solix Solarbank E1600 to MQTT

This addon uses the [anker-splix-api](https://github.com/thomluther/anker-solix-api) library to poll the Solix API for the latest sample data and publish it to an MQTT broker.

## Prerequisites

You need to have a running [MQTT broker](https://github.com/home-assistant/addons/tree/master/mosquitto) instance.

## Configuration

The add-on can be configured using the following parameters:

**user**: A Solix API client id.

**password**: The client secret.

**country**: A two-letter country code (e.g. DE).

**mqtt_uri**: The MQTT broker URL, e.g. mqtt://homeassistant.local:1883.

**mqtt_username**: Optional username for MQTT authentication.

**mqtt_password**: Optional password for MQTT authentication.

**mqtt_topic**: Topic where data will be be published.

## Installation

python3 -m venv venv
source venv/bin/activate
pip install influxdb_client aiohttp asyncio

chmod 755 solix2influxdb.sh
sudo ln -s /opt/solix2influxdb/solix2influxdb.service /etc/systemd/system/solix2influxdb.service
sudo systemctl daemon-reload


This add on is based on the great work of:

- [anker-solix-api](https://github.com/thomluther/anker-solix-api)
- [python-eufy-security](https://github.com/FuzzyMistborn/python-eufy-security)
- [solix2mqtt](https://github.com/tomquist/solix2mqtt)

## Support

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/markusmauch)
