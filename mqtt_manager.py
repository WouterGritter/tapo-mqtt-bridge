import json
from typing import Callable

import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage


class MqttManager:
    def __init__(self, mqtt_broker_address: str, mqtt_broker_port: int):
        self.mqtt_broker_address = mqtt_broker_address
        self.mqtt_broker_port = mqtt_broker_port

        self.subscribers: dict[str, Callable[[MQTTMessage], None]] = dict()

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_message = self._on_message
        self.client.on_connect = self._on_connect

    def connect(self):
        print('Connecting to MQTT...')
        self.client.connect(self.mqtt_broker_address, self.mqtt_broker_port, 60)
        self.client.loop_start()

    def publish(self, topic: str, payload: any, retain: bool, qos: int = 0):
        self.client.publish(topic, payload, qos, retain)

    def subscribe(self, topic: str, callback: Callable[[MQTTMessage], None]):
        self.subscribers[topic] = callback
        if self.client.is_connected():
            self.client.subscribe(topic)

    def unsubscribe(self, topic):
        print(f'Unsubscribing from topic {topic}.')
        self.client.unsubscribe(topic)
        del self.subscribers[topic]

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        print(f'Connected to MQTT. Subscribing to {len(self.subscribers)} topics.')
        for topic in self.subscribers.keys():
            self.client.subscribe(topic)

    def _on_message(self, client: mqtt.Client, userdata: any, message: MQTTMessage):
        topic = message.topic

        if topic in self.subscribers.keys():
            callback = self.subscribers[topic]

            try:
                callback(message)
            except Exception as ex:
                print(f'An exception occurred while processing a message for topic {message.topic}.')
                print(ex)
