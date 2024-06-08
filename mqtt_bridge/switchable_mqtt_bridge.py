from typing import Optional

from PyP100.PyP100 import Switchable
from paho.mqtt.client import MQTTMessage

from device_utils import execute_device_method
from environment import TOPIC_FORMAT
from mqtt_bridge.mqtt_bridge import MqttBridge
from mqtt_manager import MqttManager


class SwitchableMqttBridge(MqttBridge):
    def __init__(self, mqtt_manager: MqttManager, device: Switchable, name: str, protected: bool):
        self.__mqtt_manager = mqtt_manager
        self.__device = device
        self.__name = name
        self.__protected = protected

        self.__previous_mqtt_status: Optional[bool] = None

        self.__status_topic = TOPIC_FORMAT.replace('{device}', self.__name).replace('{attribute}', 'status')

        self.__mqtt_manager.subscribe(self.__status_topic, self.__mqtt_status_change)

    def update_mqtt(self):
        tapo_status = execute_device_method(self.__device, lambda d: d.get_status())
        if self.__previous_mqtt_status != tapo_status:
            self.__mqtt_manager.publish(self.__status_topic, '1' if tapo_status else '0', True)
            self.__previous_mqtt_status = tapo_status

    def __mqtt_status_change(self, message: MQTTMessage):
        mqtt_status = message.payload.decode() == '1'
        self.__previous_mqtt_status = mqtt_status

        if self.__protected or message.retain:
            return

        tapo_status = execute_device_method(self.__device, lambda d: d.get_status())
        if tapo_status != mqtt_status:
            execute_device_method(self.__device, lambda d: d.set_status(mqtt_status))
