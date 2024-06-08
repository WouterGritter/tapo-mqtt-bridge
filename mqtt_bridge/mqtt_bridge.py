from abc import ABC, abstractmethod


class MqttBridge(ABC):

    @abstractmethod
    def update_mqtt(self):
        pass
