from mqtt_bridge.mqtt_bridge import MqttBridge


class CompositeMqttBridge(MqttBridge):
    def __init__(self, bridges: list[MqttBridge]):
        self.__bridges = bridges

    def update_mqtt(self, force_update: bool = False):
        for bridge in self.__bridges:
            bridge.update_mqtt(force_update)
