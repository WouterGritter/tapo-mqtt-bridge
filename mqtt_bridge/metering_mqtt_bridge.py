from dataclasses import dataclass
from typing import Optional

from PyP100.PyP100 import Metering
from paho.mqtt.client import MQTTMessage

from device_utils import execute_device_method
from environment import generate_topic
from mqtt_bridge.mqtt_bridge import MqttBridge
from mqtt_manager import MqttManager


@dataclass
class MeteringData:
    month_energy: int
    power: float


class MeteringMqttBridge(MqttBridge):
    def __init__(self, mqtt_manager: MqttManager, device: Metering, name: str, min_power: float, power_decimals: int):
        self.__mqtt_manager = mqtt_manager
        self.__device = device
        self.__name = name
        self.__min_power = min_power
        self.__power_decimals = power_decimals

        self.__cumulative_energy: int = 0
        self.__previous_energy: Optional[int] = None
        self.__previous_power: Optional[float] = None

        self.__energy_topic = generate_topic(self.__name, 'energy')
        self.__power_topic = generate_topic(self.__name, 'power')

        self.__mqtt_manager.subscribe(self.__energy_topic, self.__mqtt_energy_change)

    def update_mqtt(self, force_update: bool = False):
        metering_data = self.__fetch_metering_data()

        if force_update or metering_data.power != self.__previous_power:
            self.__mqtt_manager.publish(self.__power_topic, metering_data.power, True)
            self.__previous_power = metering_data.power

        if self.__previous_energy is not None:
            if metering_data.month_energy < self.__previous_energy:
                # The energy counter on the tapo device has reset
                energy_delta = metering_data.month_energy
            else:
                energy_delta = metering_data.month_energy - self.__previous_energy

            self.__cumulative_energy += energy_delta

            if force_update or energy_delta > 0:
                self.__mqtt_manager.publish(self.__energy_topic, self.__cumulative_energy, True)

        self.__previous_energy = metering_data.month_energy

    def __fetch_metering_data(self) -> MeteringData:
        energy_usage = execute_device_method(self.__device, lambda d: d.getEnergyUsage())

        month_energy = energy_usage['month_energy']
        power = energy_usage['current_power'] / 1000.0
        if power < self.__min_power:
            power = 0.0

        power = round(power, self.__power_decimals)
        if self.__power_decimals <= 0:
            power = int(power)

        return MeteringData(
            month_energy=month_energy,
            power=power,
        )

    def __mqtt_energy_change(self, message: MQTTMessage):
        self.__cumulative_energy = int(message.payload.decode())
