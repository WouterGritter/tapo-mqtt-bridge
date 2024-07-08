import os

from dotenv import load_dotenv

load_dotenv()

TP_LINK_EMAIL = os.getenv('TP_LINK_EMAIL')
TP_LINK_PASSWORD = os.getenv('TP_LINK_PASSWORD')
DEVICES_CONFIG_LOCATION = os.getenv('DEVICES_CONFIG_LOCATION', 'devices.yml')
DEVICES_CONFIG = os.getenv('DEVICES_CONFIG')
MQTT_BROKER_ADDRESS = os.getenv('MQTT_BROKER_ADDRESS', 'localhost')
MQTT_BROKER_PORT = int(os.getenv('MQTT_BROKER_PORT', '1883'))
MQTT_BROKER_USERNAME = os.getenv('MQTT_BROKER_USERNAME')
MQTT_BROKER_PASSWORD = os.getenv('MQTT_BROKER_PASSWORD')
UPDATE_INTERVAL = float(os.getenv('UPDATE_INTERVAL', '5'))
FORCE_UPDATE_INTERVAL = float(os.getenv('FORCE_UPDATE_INTERVAL', '60'))
TOPIC_FORMAT = os.getenv('TOPIC_FORMAT', 'tapo/{device}/{attribute}')


def print_environment():
    print(f'{TP_LINK_EMAIL=}')
    print(f'TP_LINK_PASSWORD={hide_password(TP_LINK_PASSWORD)}')
    print(f'{DEVICES_CONFIG_LOCATION=}')
    print(f'{DEVICES_CONFIG=}')
    print(f'{MQTT_BROKER_ADDRESS=}')
    print(f'{MQTT_BROKER_PORT=}')
    print(f'{MQTT_BROKER_USERNAME=}')
    print(f'MQTT_BROKER_PASSWORD={hide_password(MQTT_BROKER_PASSWORD)}')
    print(f'{UPDATE_INTERVAL=}')
    print(f'{FORCE_UPDATE_INTERVAL=}')
    print(f'{TOPIC_FORMAT=}')


def hide_password(password):
    if password is not None:
        return '*' * len(password)
    else:
        return None


def generate_topic(device: str, attribute: str):
    return TOPIC_FORMAT.format(device=device, attribute=attribute)
