from socket import socket, AF_INET, SOCK_STREAM
from MQTTSubscriber import MQTTSubscriber
from paho.mqtt import client as mqtt_client
from json import loads, dumps
from threading import Thread
from time import sleep


import sys
sys.path.insert(0, '..')
from consts.consts import *


class Nevoa(MQTTSubscriber):
    def __init__(self, region: int, c_addr: str, c_port: int) -> None:
        super().__init__(region=region)
        self._cloud_addr: str = c_addr
        self._cloud_port: int = c_port
        self._three_best_queues: list = list()

    def edge_connect(self) -> socket:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self._cloud_addr, self._cloud_port))
        return sock

    def send_best_queue(self) -> str:
        sleep(EDGE_TIME_TO_SEND)
        sock = self.edge_connect()
        msg = dumps(self.get_best_gas_station_queue()).encode(encoding='UTF-8')
        sock.send(msg)
        response = sock.recv(1024)
        sock.close()
        return response.decode()

    # A logica do programa sera feita aqui
    def on_message(self, client: mqtt_client, user_data, msg) -> None:
        recvd_msg = loads(msg.payload.decode()).replace("'", '"')
        if self._three_best_queues.__len__() == 3:
            # Logica para atualizar os 3 melhores postos
            self._refresh_gas_station_queue(recvd_msg)
            return
        self._three_best_queues.append(recvd_msg)
        self._three_best_queues.sort(key=lambda gas_station_info: gas_station_info['queue'], reverse=False)

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
        queue_list_i = 3
        new_gas_station_id = new_gas_station_info['id']
        new_gas_station_queue = new_gas_station_info['queue']
        while queue_list_i:
            gas_station_id = self._three_best_queues[queue_list_i]['id']
            if new_gas_station_id == gas_station_id:
                self._three_best_queues[queue_list_i] = new_gas_station_info
                return
            queue_list_i -= 1
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
