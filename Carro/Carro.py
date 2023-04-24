import json
import random
import threading
import time
from uuid import uuid4
from paho.mqtt import client as mqtt_client
from socket import socket, AF_INET, SOCK_STREAM

import sys
sys.path.insert(0, '..')
from consts.consts import *


def on_connect(client, userdata, flags, rc: int) -> None:
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        raise Exception("Failure connect to Broker")


class Station:
    def __init__(self, id_station, region_station, queue_station) -> None:
        self.id: str = id_station
        self.region: int = region_station
        self.queue: str = queue_station


class Car:
    def __init__(self, cloud_addr: str, cloud_port: int) -> None:
        self._id: str = str(uuid4())
        self._region: int = random.randint(1, 3)
        self._broker_addr: str = eval(f'BROKER_REGION_{self._region}_ADDR')
        self._broker_port: int = eval(f'BROKER_REGION_{self._region}_PORT')
        self._cloud_addr: str = cloud_addr
        self._cloud_port: int = cloud_port
        self._battery_total_charge: int = 10
        self._topic: str = 'gas_station' + '/+/' + 'region' + '/' + self._region.__str__()
        self._battery_level = self._battery_total_charge
        self._best_station: Station = None

    def _connect_mqtt(self) -> mqtt_client:
        client = mqtt_client.Client()
        client.on_connect = on_connect
        client.connect(self._broker_addr, self._broker_port)
        return client

    def _socket_connect(self) -> socket:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self._cloud_addr, self._cloud_port))
        return sock

    def _mqtt_connect(self):
        client = self._connect_mqtt()
        self._subscribe(client)
        client.loop_forever()

    def _subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            station = json.loads(msg.payload.decode())
            if not self._best_station or self._best_station.queue > station.get('queue', "Tamanho da fila não encontrado"):
                self._best_station = Station(station.get('id', "Id não encontrado"),
                                             station.get('region', "Região não encontrada"),
                                             station.get('queue', "Tamanho da fila não encontrado"))
            # else:
            #     if self._best_station.queue > station.queue:
            #         self._best_station = Station(station.id, station.region, station.queue)

        client.subscribe(self._topic)
        client.on_message = on_message

    def _battery_manager(self):
        while self._battery_level != 0:
            time.sleep(1)
            self._battery_level -= 1

            if self._battery_level <= self._battery_total_charge * 0.3:
                print("Bateria descarregada")
                #implementar lógica de buscar um posto na nuvem
                print("Se dirigindo ao posto com id:", self._best_station.id, "na região:", self._best_station.region)
                time_to_recharge = self._best_station.queue * 1 + (self._battery_total_charge - self._battery_level)
                time.sleep(time_to_recharge)
                self._battery_level = self._battery_total_charge
                print("O carro acabou de ser recarregado!")
        print("O carro morreu, impossível ir até um posto")

    def _get_cloud_gas_station(self) -> str:
        car_conn = self._socket_connect()
        msg = f'{{"region_id": {self._region}, "gas_station":"best"}}'.encode(encoding='UTF-8')
        car_conn.send(msg)
        response = car_conn.recv(DEFAULT_RECV_TCP_BYTES).decode()
        return response

    def start(self):
        thread1 = threading.Thread(target=self._mqtt_connect)

        thread2 = threading.Thread(target=self._battery_manager)

        # iniciar a thread do mqtt
        thread1.start()

        # iniciar a thread de gerenciamento da bateria
        thread2.start()

if __name__ == '__main__':
    carro = Car()

    carro.start()
