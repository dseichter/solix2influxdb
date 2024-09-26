# Anker Solix Solarbank E1600 to InfluxDB

This service uses the [anker-solix-api](https://github.com/thomluther/anker-solix-api) library to poll the Solix API for the latest sample data and publish it to an InfluxDB.

## Prerequisites

You need to have a running [InfluxDB](https://www.influxdata.com/products/influxdb/) instance. On your server, python3 needs to be installed.

## Configuration

Create a file `options.json` and provide the following parameters:

```JSON
{
    "user": "your anker login name",
    "password": "your password of the anker app",
    "country": "country code (e.g. DE)",
    "poll_interval": 30,
    "influxdb_token": "<token generated in influxdb>",
    "influxdb_org": "organisation_name",
    "influxdb_bucket": "name on a newly created bucket",
    "influxdb_url": "http://127.0.0.1:8086"
}
```

## Installation

Downdload or clone the repository. Switch to the directory. E.g. /opt/solix2influxdb. 

Run the following commands:
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r src/requirements.txt
```

After that, adjust the shell script, if it is not placed into /opt/solix2influxdb

Make the script executable
```sh
chmod 755 solix2influxdb.sh
```

If you want to install it as a service, you can run the following (be aware of adjusting the service file if the path is different from /opt/solix2influxdb)

```sh
sudo ln -s /opt/solix2influxdb/solix2influxdb.service /etc/systemd/system/solix2influxdb.service
sudo systemctl daemon-reload
sudo systemctl start solix2influxdb.service
```

Check, if everything is fine by running
```sh
sudo systemctl start solix2influxdb.service
```


This add on is based on the great work of:

- [homeassistant-addons](https://github.com/markusmauch/homeassistant-addons)
- [anker-solix-api](https://github.com/thomluther/anker-solix-api)

# Feedback

You are welcome to provide feedback.