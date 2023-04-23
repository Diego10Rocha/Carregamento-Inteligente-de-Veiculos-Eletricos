from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from json import loads

import sys
sys.path.insert(0, '..')
from consts.consts import *

# A nuvem nao possui regiao, pois e um servidor central
# A nuvem sera um servidor construido em socket que implementara um protocolo
# desenvolvido por nos mesmos
# A nuvem vai receber o a informacao da melhor fila
# das nevoas, e vai guardar em uma lista (tamanho 3) os
# melhores filas de cada regiao e responder ao carro ao receber
# uma requisicao do carro, acho que o carro vai fazer uma requisicao via
# socket para a nuvem, a API será apenas para verificar o estado do carro
# por parte de quem quiser por meio do protocolo HTTP(S)

# Uma porta para a nevoa e outra porta para os carros


class Cloud:
    def __init__(self, addr: str, nevoa_port: int, car_port: int) -> None:
        self._addr: str = addr
        self._nevoa_port: int = nevoa_port
        self._car_port: int = car_port
        self._best_region_queues: list = list()

    # Ordena os melhores postos de acordo com a regiao deles
    def _sort_best_region_queues(self) -> None:
        self._best_region_queues.sort(key=lambda gas_station: gas_station['region_id'], reverse=False)

    # Devolve o socket a conexao do cliente
    def _create_nevoa_server_side(self) -> socket:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self._addr, self._nevoa_port))
        sock.listen()
        client_socket, addr = sock.accept()
        Thread(target=self._create_nevoa_server_side).start()
        return client_socket

    def _on_nevoa_recieve(self, client_socket: socket) -> None:
        print(f'CLOUD BEST REGION QUEUES -> {self._best_region_queues}')
        new_best_gas_station = loads(client_socket.recv(DEFAULT_RECV_TCP_BYTES).decode().replace("'", '"'))
        self._add_best_gas_station(new_best_gas_station)

    def _add_best_gas_station(self, new_best_gas_station) -> None:
        if len(self._best_region_queues) == 3:
            self._refresh_best_gas_stations(new_best_gas_station)
            self._sort_best_region_queues()
            return
        new_best_gas_station_region_id = new_best_gas_station['region_id']
        best_gas_station_region_ids = list(map(lambda g: g['region_id'], self._best_region_queues))
        if new_best_gas_station_region_id not in best_gas_station_region_ids:
            self._best_region_queues.append(new_best_gas_station)
            self._sort_best_region_queues()
        else:
            # Acho que nem precisa desse for
            if new_best_gas_station['id'] != self._best_region_queues[new_best_gas_station_region_id - 1]['id']:
                self._best_region_queues[new_best_gas_station_region_id - 1] = new_best_gas_station
                self._sort_best_region_queues()
            elif new_best_gas_station['queue'] != self._best_region_queues[new_best_gas_station_region_id - 1]['queue']:
                self._best_region_queues[new_best_gas_station_region_id - 1] = new_best_gas_station
                self._sort_best_region_queues()

    def _refresh_best_gas_stations(self, new_best_gas_station: dict) -> None:
        new_best_gas_station_region_id = new_best_gas_station['region_id']
        new_best_gas_station_queue = new_best_gas_station['queue']
        old_best_gas_station = self._best_region_queues[new_best_gas_station_region_id - 1]
        old_best_gas_station_queue = old_best_gas_station['queue']
        if old_best_gas_station_queue > new_best_gas_station_queue:
            self._best_region_queues[new_best_gas_station_region_id - 1] = new_best_gas_station

    def _create_car_server_side(self) -> socket:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((self._addr, self._car_port))
        sock.listen()
        client_socket, addr = sock.accept()
        Thread(target=self._create_car_server_side).start()
        return client_socket

    # Responder para o carro o melhor posto com base na regiao
    # que ele esta
    # Depois de receber a requisicao do carro eu preciso retornar
    # o melhor posto para ele.
    def _on_car_recieve(self, client_socket) -> None:
        car_request = loads(client_socket.recv(DEFAULT_RECV_TCP_BYTES).decode())
        msg = self._generate_car_response(car_request)
        client_socket.send(msg.encode(encoding='UTF-8'))
        client_socket.close()

    def _generate_car_response(self, car_request: dict) -> str:
        car_region_id = car_request['region_id']
        best_gas_station = self._best_region_queues[car_region_id - 1]
        best_gas_station_queue = best_gas_station['queue']
        best_gas_station_id = best_gas_station['id']
        msg = f'{{"status":"ok", "best_gas_station_id": "{best_gas_station_id}", "queue": {best_gas_station_queue}}}'
        return msg

    def _server_nevoa_on(self) -> None:
        nevoa_socket = self._create_nevoa_server_side()
        print(f'BEST REGION QUEUES -> {self._best_region_queues}')
        self._on_nevoa_recieve(nevoa_socket)

    def _server_car_on(self) -> None:
        car_socket = self._create_car_server_side()
        self._on_car_recieve(car_socket)

    def start_cloud(self) -> None:
        thread1 = Thread(target=self._server_nevoa_on)
        thread2 = Thread(target=self._server_car_on)
        thread1.start()
        thread2.start()
