# tapo-mqtt-bridge

A script to publish tapo device data to MQTT, and subscribe to topics to control tapo devices.

## Supported devices

- P110/P115 (tested, full control and monitoring)
- P100 (untested, full control and monitoring)
- L530 (untested, only metering and switching)

## Configuration

The script expects the following environment variables to be present:

| Environment variable      | Default value                                                            | Notes                                                                            | Required? |
|---------------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------------------|-----------|
| `TP_LINK_EMAIL`           | no default                                                               |                                                                                  | yes       |
| `TP_LINK_PASSWORD`        | no default                                                               |                                                                                  | yes       |
| `DEVICES_CONFIG_LOCATION` | `devices.yml` (standalone), `/etc/tapo-mqtt-bridge/devices.yml` (docker) | Supports JSON as well as YAML, ignored if `DEVICES_CONFIG` is present            | no        |
| `DEVICES_CONFIG`          | no default                                                               | Supports JSON only                                                               | no        |
| `MQTT_BROKER_ADDRESS`     | `localhost`                                                              |                                                                                  | no        |
| `MQTT_BROKER_PORT`        | `1883`                                                                   |                                                                                  | no        |
| `MQTT_BROKER_USERNAME`    | no default                                                               |                                                                                  | no        |
| `MQTT_BROKER_PASSWORD`    | no default                                                               |                                                                                  | no        |
| `UPDATE_INTERVAL`         | `5` seconds                                                              | Interval between MQTT publishes if value is different compared to previous value | no        |
| `FORCE_UPDATE_INTERVAL`   | `60` seconds                                                             | Interval between MQTT publishes regardless of if value is different              | no        |
| `TOPIC_FORMAT`            | `tapo/{device}/{attribute}`                                              |                                                                                  | no        |

The script expects a `devices.yml` file to be present in the app root (when running standalone) or at `/etc/tapo-mqtt-bridge/devices.yml` (when running in docker) by default. But, this location can be changed using the `DEVICES_CONFIG_LOCATION` environment variable and also supports a `.json` file.

When the `DEVICES_CONFIG` environment variable is present, the script does not load any file and loads the device configuration through the environment variable instead. This environment variable should be in JSON format.

Example configuration (see also `devices.example.yml` and `devices.example.json`):
```yaml
devices:
  # The name of the device to use for publishing/subscribing to MQTT topics
  server-rack:
    # The address of the device
    address: '10.43.60.112'
    # The type of the tapo device (P100, P110, P115, L530)
    type: 'P110'
    # Whether the device is protected or not, meaning publishing to its topics will not result in status changes of the device
    protected: true
    # (Optional) email to use when authenticating with TP-Link. When absent, the environment variable `TP_LINK_EMAIL` is used.
    # May reference an environment variable when prefixed with '$', e.g. '$TP_LINK_EMAIL'
    email: $TP_LINK_EMAIL
    # (Optional) password to use when authenticating with TP-Link. When absent, the environment variable `TP_LINK_PASSWORD` is used.
    # May reference an environment variable when prefixed with '$', e.g. '$TP_LINK_PASSWORD'
    password: $TP_LINK_PASSWORD
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

Switchable devices publish and subscribe to `tapo/<device_name>/status` by default, and expect/publish a '1' and a '0' as the value.

**Metering devices**

Metering devices publish to `tapo/<device_name>/power` and `tapo/<device_name>/energy` by default. They also subscribe to the energy endpoint to allow persistence of data.

Note that metering devices do not publish the daily or monthly energy data as provided by the tapo API. The script calculates the difference between energy measurements, resulting in an absolute energy measurement being available on the MQTT broker. A limitation of this approach is that the energy consumption between server restarts will be missing.

**Color devices**

Changing the color and brightness of color devices is currently unsupported, as I do not own such light bulbs to test with.
