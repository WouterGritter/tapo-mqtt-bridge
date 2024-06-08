import json
import time

import yaml
from PyP100.PyL530 import L530
from PyP100.PyP100 import P100
from PyP100.PyP110 import P110

from environment import MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT, TP_LINK_EMAIL, TP_LINK_PASSWORD, DEVICES_CONFIG_LOCATION, \
    UPDATE_INTERVAL, print_environment
from mqtt_bridge.mqtt_bridge import MqttBridge
from mqtt_bridge.p100_mqtt_bridge import P100MqttBridge
from mqtt_bridge.p530_mqtt_bridge import L530MqttBridge
from mqtt_manager import MqttManager
from mqtt_bridge.p110_mqtt_bridge import P110MqttBridge


MQTT_MANAGER = MqttManager(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT)


def load_mqtt_bridges(file_name: str) -> list[MqttBridge]:
    if file_name.endswith('.yml') or file_name.endswith('.yaml'):
        with open(file_name) as stream:
            config = yaml.safe_load(stream)
    elif file_name.endswith('.json'):
        with open(file_name) as stream:
            config = json.load(stream)

    bridges = []
    devices = config['devices']
    for name, device_config in devices.items():
        bridges.append(create_mqtt_bridge(name, device_config))

    return bridges


def create_mqtt_bridge(name: str, config: dict[str, any]) -> MqttBridge:
    if config['type'] == 'P110':
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


def main():
    print_environment()

    bridges = load_mqtt_bridges(DEVICES_CONFIG_LOCATION)
    print(f'Loaded {len(bridges)} device bridges.')

    MQTT_MANAGER.connect()

    while True:
        time.sleep(UPDATE_INTERVAL)
        for bridge in bridges:
            try:
                bridge.update_mqtt()
            except Exception as ex:
                print(f'An exception occurred while updating a device.')
                print(ex)


if __name__ == '__main__':
    main()
