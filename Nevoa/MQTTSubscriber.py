import sys
from paho.mqtt import client as mqtt_client
from uuid import uuid4
from abc import ABC, abstractmethod
sys.path.insert(0, '..')
from consts.consts import BROKER_ADDR, BROKER_PORT


# Codigo executado ao receber uma mensagem do broker


def on_connect(client, userdata, flags, rc: int) -> None:
    if not rc:
        print('Connected to MQTT Broker!')
    else:
        raise Exception('Failde to connect to MQTT Broker!')

class MQTTSubscriber(ABC):
    def __int__(self, region: int) -> None:
        self._id = uuid4().__str__()
        self._region_id: int = region
        self._topic: str = f'gas_station/region/{self._region_id}/id/{self._id}'
        self._broker_addr: str = eval(f'BROKER_REGION_{self._region_id}_ADDR')
        self._broker_port: int = eval(f'BROKER_REGION_{self._region_id}_PORT')

    def connect_mqtt(self) -> mqtt_client:
        client = mqtt_client.Client(self._id)
        client.on_connect = on_connect
        client.connect(self._broker_addr, self._broker_port)
        return client

    def subscribe(self, client: mqtt_client) -> None:
        client.subscribe(self._topic)
        client.on_message = self.on_message

    # Talvez isso precise rodar em uma thread separada
    # do socket
    def subscriber_run(self) -> None:
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()

    @abstractmethod
    def on_message(self, client: mqtt_client, user_data, msg) -> str:
        pass
