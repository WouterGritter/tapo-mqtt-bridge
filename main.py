import json
import time

import yaml
from PyP100.PyL530 import L530
from PyP100.PyP100 import P100
from PyP100.PyP110 import P110

from environment import MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, MQTT_BROKER_USERNAME, MQTT_BROKER_PASSWORD, \
    TP_LINK_EMAIL, TP_LINK_PASSWORD, DEVICES_CONFIG_LOCATION, \
    DEVICES_CONFIG, UPDATE_INTERVAL, FORCE_UPDATE_INTERVAL, print_environment
from mqtt_bridge.mqtt_bridge import MqttBridge
from mqtt_bridge.p100_mqtt_bridge import P100MqttBridge
from mqtt_bridge.p530_mqtt_bridge import L530MqttBridge
from mqtt_manager import MqttManager
from mqtt_bridge.p110_mqtt_bridge import P110MqttBridge

MQTT_MANAGER = MqttManager(
    mqtt_broker_address=MQTT_BROKER_ADDRESS,
    mqtt_broker_port=MQTT_BROKER_PORT,
    mqtt_username=MQTT_BROKER_USERNAME,
    mqtt_password=MQTT_BROKER_PASSWORD
)


def load_mqtt_bridges() -> list[MqttBridge]:
    if DEVICES_CONFIG is not None:
        print('Loading devices from DEVICES_CONFIG environment variable.')
        config = json.loads(DEVICES_CONFIG)
    else:
        print(f'Loading devices from the file {DEVICES_CONFIG_LOCATION}.')
        file_name = DEVICES_CONFIG_LOCATION
        if file_name.endswith('.yml') or file_name.endswith('.yaml'):
            with open(file_name) as stream:
                config = yaml.safe_load(stream)
        elif file_name.endswith('.json'):
            with open(file_name) as stream:
                config = json.load(stream)
        else:
            raise Exception('Invalid device configuration file extension.')

    bridges = []
    devices = config['devices']
    for name, device_config in devices.items():
        bridges.append(create_mqtt_bridge(name, device_config))

    return bridges


def create_mqtt_bridge(name: str, config: dict[str, any]) -> MqttBridge:
    if config['type'] == 'P110' or config['type'] == 'P115':
        return P110MqttBridge(
            MQTT_MANAGER,
            P110(config['address'], TP_LINK_EMAIL, TP_LINK_PASSWORD),
            name,
            config['protected'],
        )
    elif config['type'] == 'P100':
        return P100MqttBridge(
            MQTT_MANAGER,
            P100(config['address'], TP_LINK_EMAIL, TP_LINK_PASSWORD),
            name,
            config['protected'],
        )
    elif config['type'] == 'L530':
        return L530MqttBridge(
            MQTT_MANAGER,
            L530(config['address'], TP_LINK_EMAIL, TP_LINK_PASSWORD),
            name,
            config['protected'],
        )

    raise Exception(f'Unknown device type \'{config["type"]}\'')


def update_bridges(bridges: list[MqttBridge], force_update: bool):
    for bridge in bridges:
        try:
            bridge.update_mqtt(force_update)
        except Exception as ex:
            print(f'An exception occurred while updating a device.')
            print(ex)


def main():
    print_environment()

    bridges = load_mqtt_bridges()
    print(f'Loaded {len(bridges)} device bridges.')

    MQTT_MANAGER.connect()

    time.sleep(UPDATE_INTERVAL)

    last_force_update = 0
    while True:
        now = time.time()
        force_update = now - last_force_update >= FORCE_UPDATE_INTERVAL
        if force_update:
            last_force_update = now

        start = now
        update_bridges(bridges, force_update)
        elapsed = time.time() - start

        time.sleep(max(0, UPDATE_INTERVAL - elapsed))


if __name__ == '__main__':
    main()
