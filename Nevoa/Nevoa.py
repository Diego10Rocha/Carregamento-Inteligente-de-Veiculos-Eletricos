from socket import socket, AF_INET, SOCK_STREAM
from paho.mqtt import client as mqtt_client
from json import loads, dumps
from threading import Thread
from time import sleep
from uuid import uuid4
from consts import *


def on_connect(client, userdata, flags, rc: int) -> None:
    if not rc:
        print('Connected to MQTT Broker!')
    else:
        raise Exception('Failde to connect to MQTT Broker!')


class Nevoa:
    def __init__(self, region_id: int, cloud_addr: str, cloud_port: int) -> None:
        self._id = uuid4().__str__()
        self._region_id: int = region_id
        self._topic: str = f'gas_station/region/{self._region_id}/id/+'
        self._broker_addr: str = eval(f'BROKER_REGION_{self._region_id}_ADDR')
        self._broker_port: int = eval(f'BROKER_REGION_{self._region_id}_PORT')
        self._cloud_addr: str = cloud_addr
        self._cloud_port: int = cloud_port
        self._three_best_queues: list = list()

    def connect_mqtt(self) -> mqtt_client:
        client = mqtt_client.Client(self._id)
        client.on_connect = on_connect
        client.connect(self._broker_addr, self._broker_port)
        return client

    def subscribe(self, client: mqtt_client) -> None:
        client.subscribe(self._topic)
        client.on_message = self.on_message

    def subscriber_run(self) -> None:
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()

    def edge_connect(self) -> socket:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self._cloud_addr, self._cloud_port))
        return sock

    def send_best_queue(self) -> None:
        while True:
            sleep(EDGE_TIME_TO_SEND)
            if self._three_best_queues:
                sock = self.edge_connect()
                best_gas_station = self.get_best_gas_station_queue()
                gas_stat_queue = best_gas_station['queue']
                gas_stat_region_id = best_gas_station['region_id']
                gas_stat_id = best_gas_station['id']
                msg = f'{{"region_id": {gas_stat_region_id}, "gas_station_id": "{gas_stat_id}", "queue": {gas_stat_queue}}}'
                sock.send(msg.encode(encoding='UTF-8'))
                sock.close()

    def _sort_three_best_queues(self) -> None:
        self._three_best_queues.sort(key=lambda gas_station_info: gas_station_info['queue'], reverse=False)

    # A logica do programa sera feita aqui
    def on_message(self, client: mqtt_client, user_data, msg) -> None:
        print(f'BEST QUEUES -> {self._three_best_queues}')
        new_gas_station = loads(msg.payload.decode())
        self._add_gas_station(new_gas_station)

    def _add_gas_station(self, new_gas_station: dict) -> None:
        if self._three_best_queues.__len__() == 3:
            # Logica para atualizar os 3 melhores postos
            self._refresh_gas_station_queue(new_gas_station)
            self._sort_three_best_queues()
            return
        new_gas_station_id = new_gas_station['id']
        three_best_queues_ids = list(map(lambda g: g['id'], self._three_best_queues))
        if new_gas_station_id not in three_best_queues_ids:
            self._three_best_queues.append(new_gas_station)
            self._sort_three_best_queues()
        else:
            for i in range(len(self._three_best_queues)):
                if self._three_best_queues[i]['id'] == new_gas_station_id:
                    self._three_best_queues[i] = new_gas_station
                    break
            self._sort_three_best_queues()

    # A funcao subscribe serve como um gatilho
    # para executar toda a logica do programa
    # ao receber uma mensagem do broker
    def get_best_gas_station_queue(self) -> dict:
        return self._three_best_queues[0]

    # Ordena os postos de acordo com as suas filas
    # O posto com a menor fila ficara na primeira posicao
    # da fila (0)
    # Verifica se a informacao nova nao e de um posto que ja existe,
    # se for de um posto que ja existe e for igual, matem, caso contrario
    # atualiza a nova fila.
    def _refresh_gas_station_queue(self, new_gas_station_info: dict) -> None:
        queue_list_i = len(self._three_best_queues) - 1
        new_gas_station_id = new_gas_station_info['id']
        new_gas_station_queue = new_gas_station_info['queue']
        while queue_list_i > -1:
            gas_station_id = self._three_best_queues[queue_list_i]['id']
            if new_gas_station_id == gas_station_id:
                self._three_best_queues[queue_list_i] = new_gas_station_info
                return
            queue_list_i -= 1
        queue_list_i = 0
        while queue_list_i < 3:
            gas_station_queue = self._three_best_queues[queue_list_i]['queue']
            if gas_station_queue > new_gas_station_queue:
                self._three_best_queues[queue_list_i] = new_gas_station_info
                return
            queue_list_i += 1

    def run(self) -> None:
        thread1 = Thread(target=self.subscriber_run)
        thread2 = Thread(target=self.send_best_queue)
        thread1.start()
        thread2.start()
