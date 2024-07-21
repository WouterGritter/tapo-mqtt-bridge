from PyP100.PyP110 import P110

from mqtt_bridge.composite_mqtt_bridge import CompositeMqttBridge
from mqtt_bridge.metering_mqtt_bridge import MeteringMqttBridge
from mqtt_bridge.switchable_mqtt_bridge import SwitchableMqttBridge
from mqtt_manager import MqttManager


class P110MqttBridge(CompositeMqttBridge):
    def __init__(self, mqtt_manager: MqttManager, device: P110, name: str, protected: bool, min_power: float, power_decimals: int):
        super().__init__([
            SwitchableMqttBridge(mqtt_manager, device, name, protected),
            MeteringMqttBridge(mqtt_manager, device, name, min_power, power_decimals),
        ])
