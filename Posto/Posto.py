from uuid import uuid4
from random import randint
import paho.mqtt.client as mqtt_client
from time import sleep
from threading import Thread

from consts import *


# O posto vai criar um topico no broker
# e enviar as informacoes da fila dele para
# este topico

# Cada posto tera um codigo (uuid4)
# Um topico para cada posto
# A mensagem enviada e um numero inteiro, que corresponde
# a fila atual do posto
# O posto envia a sua coordenada para os servidores da nevoa


# O posto pertence a uma regiao pre-determinada
# o programa cobrira no maximo 3 regioes


# Apos iniciar, o posto so vai ficar enviando as informacoes da fila
# dele para a nevoa para o topico dele. Dessa forma, a fila mudara a cada
# X segundos

def on_connect(rc: int) -> None:
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        raise Exception("Failure connect to Broker")


class Posto:
    def __init__(self, region_id: int) -> None:
        self._id: str = uuid4().__str__()
        self.region_id: int = region_id
        self._broker_addr: str = eval(f'BROKER_REGION_{self.region_id}_ADDR')
        self._broker_port: int = eval(f'BROKER_REGION_{self.region_id}_PORT')
        self._queue: int = randint(0, 100)
        self._topic: str = f'gas_station/region/{self.region_id}/id/{self._id}'

    def _connect_mqtt(self) -> mqtt_client:
        client = mqtt_client.Client()
        client.on_connect = on_connect
        client.connect(self._broker_addr, self._broker_port)
        return client

    def _publish(self, client: mqtt_client) -> None:
        print(self._topic)
        while True:
            sleep(GAS_STATION_TIME_TO_SEND)
            topic = self._topic
            msg = f'{{"region_id": {self.region_id}, "id": "{self._id.__str__()}", "queue": {self._queue}}}'
            result = client.publish(topic, msg)
            status = result[0]
            print('Failed to send message') if status else print('Successful send message')

    def start(self) -> None:
        client = self._connect_mqtt()
        thread1 = Thread(target=self._publish, args=(client,))
        thread2 = Thread(target=self._refresh_queue)
        thread1.start()
        thread2.start()

    def _refresh_queue(self) -> None:
        while True:
            sleep(GAS_STATION_TIME_TO_REFRESH)
            self._queue = randint(0, 100)
