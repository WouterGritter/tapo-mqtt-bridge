from PyP100.PyP100 import P100

from mqtt_bridge.composite_mqtt_bridge import CompositeMqttBridge
from mqtt_bridge.switchable_mqtt_bridge import SwitchableMqttBridge
from mqtt_manager import MqttManager


class P100MqttBridge(CompositeMqttBridge):
    def __init__(self, mqtt_manager: MqttManager, device: P100, name: str, protected: bool):
        super().__init__([
            SwitchableMqttBridge(mqtt_manager, device, name, protected),
        ])

        self.device = device
        self.name = name

    def __str__(self):
        return f'P100MqttBridge[name={self.name}, device.address={self.device.address}]'
