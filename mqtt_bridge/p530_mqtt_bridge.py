from PyP100.PyL530 import L530

from mqtt_bridge.composite_mqtt_bridge import CompositeMqttBridge
from mqtt_bridge.metering_mqtt_bridge import MeteringMqttBridge
from mqtt_bridge.switchable_mqtt_bridge import SwitchableMqttBridge
from mqtt_manager import MqttManager


class L530MqttBridge(CompositeMqttBridge):
    def __init__(self, mqtt_manager: MqttManager, device: L530, name: str, protected: bool):
        super().__init__([
            MeteringMqttBridge(mqtt_manager, device, name),
            SwitchableMqttBridge(mqtt_manager, device, name, protected),
        ])
