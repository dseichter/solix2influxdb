#!/usr/bin/env bash
set -e

source venv/bin/activate

CONFIG_PATH=options.json

export S2M_USER=$(jq --raw-output '.user // empty' $CONFIG_PATH)
export S2M_PASSWORD=$(jq --raw-output '.password // empty' $CONFIG_PATH)
export S2M_COUNTRY=$(jq --raw-output '.country // empty' $CONFIG_PATH)
export S2M_MQTT_URI=$(jq --raw-output '.mqtt_uri // empty' $CONFIG_PATH)
export S2M_MQTT_USERNAME=$(jq --raw-output '.mqtt_username // empty' $CONFIG_PATH)
export S2M_MQTT_PASSWORD=$(jq --raw-output '.mqtt_password // empty' $CONFIG_PATH)
export S2M_MQTT_TOPIC=$(jq --raw-output '.mqtt_topic // empty' $CONFIG_PATH)
export S2M_POLL_INTERVAL=$(jq --raw-output '.poll_interval // 30' $CONFIG_PATH)

export INFLUXDB_TOKEN=$(jq --raw-output '.influxdb_token // empty' $CONFIG_PATH)
export INFLUXDB_URL=$(jq --raw-output '.influxdb_url // empty' $CONFIG_PATH)
export INFLUXDB_ORG=$(jq --raw-output '.influxdb_org // empty' $CONFIG_PATH)
export INFLUXDB_BUCKET=$(jq --raw-output '.influxdb_bucket // empty' $CONFIG_PATH)

export S2M_VERBOSE=true

python3 src/solix2mqtt.py
