import asyncio
import logging
import os
import random
import sys
import time
from aiohttp import ClientSession
from api import api

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

_LOGGER: logging.Logger = logging.getLogger(__name__)
_LOGGER.addHandler(logging.StreamHandler(sys.stdout))
CONSOLE: logging.Logger = logging.getLogger("console")
CONSOLE.addHandler(logging.StreamHandler(sys.stdout))
CONSOLE.setLevel(logging.DEBUG)

S2M_USER = os.getenv( "S2M_USER" )
S2M_PASSWORD = os.getenv( "S2M_PASSWORD" )
S2M_COUNTRY = os.getenv( "S2M_COUNTRY" )
S2M_POLL_INTERVAL = int(os.getenv("S2M_POLL_INTERVAL"))

CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}'
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

influxdb_token = os.environ.get("INFLUXDB_TOKEN", "no-token")
influxdb_url = os.environ.get("INFLUXDB_URL", "http://localhost:8086/")
influxdb_org = os.environ.get("INFLUXDB_ORG", "solar")
influxdb_bucket = os.environ.get("INFLUXDB_BUCKET", "anker")


def print_env():
    print(f"S2M_USER: {S2M_USER}")
    print(f"S2M_PASSWORD: {S2M_PASSWORD}")
    print(f"S2M_COUNTRY: {S2M_COUNTRY}")

    print(f"S2M_POLL_INTERVAL: {S2M_POLL_INTERVAL}")

    print(f"CLIENT_ID: {CLIENT_ID}")
    print(f"FIRST_RECONNECT_DELAY: {FIRST_RECONNECT_DELAY}")
    print(f"RECONNECT_RATE: {RECONNECT_RATE}")
    print(f"MAX_RECONNECT_COUNT: {MAX_RECONNECT_COUNT}")
    print(f"MAX_RECONNECT_DELAY: {MAX_RECONNECT_DELAY}")


def get_site_id(site_list, site_name):
    for site in site_list:
        if site["site_name"] == site_name:
            return site["site_id"]
    return None

async def fetch_and_publish_sites(solix: api.AnkerSolixApi, site_list):
    for site in site_list.get("site_list"):
        site_id = site["site_id"]

        # Site Info
        # site_homepage = await solix.get_homepage()
        # site_homepage_json = json.dumps( site_homepage )

        # Scene Info
        scene_info = await solix.get_scene_info(siteId=site_id)
        #scene_info_json = json.dumps( scene_info )
        
        # Direct InfluxDB write
        point = Point("solix")

        data = scene_info
        solix_info = data["solarbank_info"]

        point.tag("solarbattery", solix_info["solarbank_list"][0]["device_name"])
        for key, value in solix_info["solarbank_list"][0].items():
            try:
                point.field(key, float(value))
            except ValueError:
                point.field(key, value)
                  
        with InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org) as influxdbclient:
            with influxdbclient.write_api(write_options=SYNCHRONOUS) as writer:
                try:
                    writer.write(bucket=influxdb_bucket, record=[point])
                except Exception as e:
                    print(e)
        
        # Device Params       
        # device_param = await solix.get_device_parm(siteId=site_id)
        # device_param_json = json.dumps( device_param )


async def main() -> None:
    try:
        async with ClientSession() as websession:
            print("Starting main")
            solix = api.AnkerSolixApi(
                S2M_USER, S2M_PASSWORD, S2M_COUNTRY, websession, _LOGGER
            )

            site_list = await solix.get_site_list()

            while True:
                await fetch_and_publish_sites(solix, site_list)
                time.sleep(S2M_POLL_INTERVAL)

    except Exception as exception:
        CONSOLE.info(f"{type(exception)}: {exception}")

# run async main
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        CONSOLE.info(f"{type(err)}: {err}")
