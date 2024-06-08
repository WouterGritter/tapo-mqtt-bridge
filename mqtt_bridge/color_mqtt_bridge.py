from PyP100.PyP100 import Color

from mqtt_bridge.mqtt_bridge import MqttBridge
from mqtt_manager import MqttManager


class ColorMqttBridge(MqttBridge):
    def __init__(self, mqtt_manager: MqttManager, device: Color, name: str, protected: bool):
        self.__mqtt_manager = mqtt_manager
        self.__device = device
        self.__name = name
        self.__protected = protected

    def update_mqtt(self):
        pass
