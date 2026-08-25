import asyncio
import atexit
import json
import os
from pathlib import Path

from awscrt import mqtt
from awsiot import mqtt_connection_builder
from dotenv import load_dotenv


load_dotenv()


class PubSubClient:
    def __init__(self):
        self.endpoint = self._required_env("AWS_IOT_ENDPOINT")
        self.client_id = self._required_env("AWS_IOT_CLIENT_ID")
        self.topic = self._required_env("AWS_IOT_TOPIC")
        self.cert_path = self._required_file("AWS_IOT_CERT_PATH")
        self.private_key_path = self._required_file("AWS_IOT_PRIVATE_KEY_PATH")
        self.root_ca_path = self._required_file("AWS_IOT_ROOT_CA_PATH")
        self._connected = False

        self.publisher = mqtt_connection_builder.mtls_from_path(
            endpoint=self.endpoint,
            cert_filepath=self.cert_path,
            pri_key_filepath=self.private_key_path,
            ca_filepath=self.root_ca_path,
            client_id=self.client_id,
            clean_session=True,
            keep_alive_secs=30,
            on_connection_interrupted=self._on_connection_interrupted,
            on_connection_resumed=self._on_connection_resumed,
        )

        self.publisher.connect().result()
        self._connected = True
        atexit.register(self.disconnect)
        print(f"Connected to AWS IoT Core: {self.endpoint}")

    async def publish_async(self, car_data: dict):
        await asyncio.to_thread(self.publish, car_data)

    def publish(self, car_data: dict):
        payload = json.dumps(car_data, ensure_ascii=False).encode("utf-8")
        publish_future, packet_id = self.publisher.publish(
            topic=self.topic,
            payload=payload,
            qos=mqtt.QoS.AT_LEAST_ONCE,
        )
        publish_future.result()
        print(f"Published MQTT packet ID: {packet_id}")

    def disconnect(self):
        if not self._connected:
            return

        self.publisher.disconnect().result()
        self._connected = False
        print("Disconnected from AWS IoT Core")

    @staticmethod
    def _required_env(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise ValueError(f"Environment variable {name} is required")
        return value

    @classmethod
    def _required_file(cls, name: str) -> str:
        path = Path(cls._required_env(name)).expanduser()
        if not path.is_file():
            raise FileNotFoundError(f"{name} does not point to a file: {path}")
        return str(path)

    @staticmethod
    def _on_connection_interrupted(connection, error, **kwargs):
        print(f"AWS IoT Core connection interrupted: {error}")

    @staticmethod
    def _on_connection_resumed(connection, return_code, session_present, **kwargs):
        print(
            "AWS IoT Core connection resumed: "
            f"return_code={return_code}, session_present={session_present}"
        )
