import os

from dotenv import load_dotenv

load_dotenv()

TP_LINK_EMAIL = os.getenv('TP_LINK_EMAIL')
TP_LINK_PASSWORD = os.getenv('TP_LINK_PASSWORD')
DEVICES_CONFIG_LOCATION = os.getenv('DEVICES_CONFIG_LOCATION', 'devices.yml')
MQTT_BROKER_ADDRESS = os.getenv('MQTT_BROKER_ADDRESS', 'localhost')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', '1883'))
UPDATE_INTERVAL = float(os.getenv('UPDATE_INTERVAL', '5'))
TOPIC_FORMAT = os.getenv('TOPIC_FORMAT', 'tapo/{device}/{attribute}')


def print_environment():
    print(f'{TP_LINK_EMAIL=}')
    print(f'TP_LINK_PASSWORD={"*" * len(TP_LINK_PASSWORD)}')
    print(f'{DEVICES_CONFIG_LOCATION=}')
    print(f'{MQTT_BROKER_ADDRESS=}')
    print(f'{MQTT_BROKER_PORT=}')
    print(f'{UPDATE_INTERVAL=}')
    print(f'{TOPIC_FORMAT=}')
