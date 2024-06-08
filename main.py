import os
import time

import yaml
from PyP100.PyL530 import L530
from PyP100.PyP100 import P100
from PyP100.PyP110 import P110
from dotenv import load_dotenv

from mqtt_bridge.mqtt_bridge import MqttBridge
from mqtt_bridge.p100_mqtt_bridge import P100MqttBridge
from mqtt_bridge.p530_mqtt_bridge import L530MqttBridge
from mqtt_manager import MqttManager
from mqtt_bridge.p110_mqtt_bridge import P110MqttBridge

load_dotenv()

TP_LINK_EMAIL = os.getenv('TP_LINK_EMAIL')
TP_LINK_PASSWORD = os.getenv('TP_LINK_PASSWORD')
DEVICES_CONFIG_LOCATION = os.getenv('DEVICES_CONFIG_LOCATION', 'devices.yml')
MQTT_BROKER_ADDRESS = os.getenv('MQTT_BROKER_ADDRESS', 'localhost')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', '1883'))
UPDATE_INTERVAL = float(os.getenv('UPDATE_INTERVAL', '5'))
TOPIC_FORMAT = os.getenv('TOPIC_FORMAT', 'tapo/{device}/{attribute}')

print(f'{TP_LINK_EMAIL=}')
print(f'TP_LINK_PASSWORD={"*" * len(TP_LINK_PASSWORD)}')
print(f'{DEVICES_CONFIG_LOCATION=}')
print(f'{MQTT_BROKER_ADDRESS=}')
print(f'{MQTT_BROKER_PORT=}')
print(f'{UPDATE_INTERVAL=}')
print(f'{TOPIC_FORMAT=}')

MQTT_MANAGER = MqttManager(MQTT_BROKER_ADDRESS, MQTT_BROKER_PORT)


def load_mqtt_bridges(file_name: str) -> list[MqttBridge]:
    bridges = []
    with open(file_name) as stream:
        config = yaml.safe_load(stream)
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
