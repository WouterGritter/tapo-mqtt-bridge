# tapo-mqtt-bridge

A script to publish tapo device data to MQTT, and subscribe to topics to control tapo devices.

## Supported devices

- P110 (tested, full control and monitoring)
- P110 (untested, full control and monitoring)
- L530 (untested, only metering and switching)

## Configuration

The script expects the following environment variables to be present:
- `TP_LINK_EMAIL`
- `TP_LINK_PASSWORD`
- `DEVICES_CONFIG_LOCATION` (defaults to `devices.yml`)
- `DEVICES_CONFIG` (defaults to nothing, see below)
- `MQTT_BROKER_ADDRESS` (defaults to `localhost`)
- `MQTT_BROKER_PORT` (defaults to `1883`)
- `UPDATE_INTERVAL` (defaults to `5` seconds)
- `TOPIC_FORMAT` (defaults to `tapo/{device}/{attribute}`)

The script expects a `devices.yml` file to be present in the app root by default. But, this location can be changed using the `DEVICES_CONFIG_LOCATION` environment variable and also supports a `.json` file.

In the provided `docker-compose.yml` file, the location is changed to `/etc/tapo-mqtt-bridge/devices.yml`.

When the `DEVICES_CONFIG` environment variable is present, the script does not load any file and loads the device configuration through the environment variable instead. This environment variable should be in JSON format.

Example configuration (see also `devices.example.yml` and `devices.example.json`):
```yaml
devices:
  # The name of the device to use for publishing/subscribing to MQTT topics
  server-rack:
    # The address of the device
    address: '10.43.60.112'
    # The type of the tapo device (P100, P110, L530)
    type: 'P110'
    # Whether the device is protected or not, meaning publishing to its topics will not result in status changes of the device
    protected: true
  tv-setup:
    address: '10.43.60.72'
    type: 'P110'
    protected: false
  boiler:
    address: '10.43.60.69'
    type: 'P110'
    protected: false
```

## MQTT topics

**Switchable devices**

Switchable devices publish and subscribe to `tapo/<device_name>/status`, and expect/publish a '1' and a '0' as the value.

**Metering devices**

Metering devices publish to `tapo/<device_name>/power` and `tapo/<device_name>/energy`. They also subscribe to the energy endpoint to allow persistence of data.

Note that metering devices do not publish the daily or monthly energy data as provided by the tapo API. The script calculates the difference between energy measurements, resulting in an absolute energy measurement being available on the MQTT broker. A limitation of this approach is that the energy consumption between server restarts will be missing.

**Color devices**

Changing the color and brightness of color devices is currently unsupported, as I do not own such light bulbs to test with.
