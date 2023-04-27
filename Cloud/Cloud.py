from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from json import loads

from consts import *

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
        self._socket_nevoa: socket = None
        self._socket_car: socket = None
        self._addr: str = addr
        self._nevoa_port: int = nevoa_port
        self._car_port: int = car_port
        self._best_region_queues: list = list()

    # Ordena os melhores postos de acordo com a regiao deles
    def _sort_best_region_queues(self) -> None:
        self._best_region_queues.sort(key=lambda gas_station: gas_station['region_id'], reverse=False)

    # Instancia um socket TCP do tipo server para a nevoa
    def create_server_nevoa(self) -> None:
        self._socket_nevoa = socket(AF_INET, SOCK_STREAM)
        self._socket_nevoa.bind((self._addr, self._nevoa_port))
        self._socket_nevoa.listen()

    # Instancia um socket TCP do tipo server para  o carro
    def create_server_car(self) -> None:
        self._socket_car = socket(AF_INET, SOCK_STREAM)
        self._socket_car.bind((self._addr, self._car_port))
        self._socket_car.listen()

    # Devolve o socket a conexao do cliente
    def _create_nevoa_server_side(self) -> socket:
        #print("Servidor criado para a nevoa na porta:", self._nevoa_port)
        client_socket, addr = self._socket_nevoa.accept()
        Thread(target=self._create_nevoa_server_side).start()
        self._on_nevoa_recieve(client_socket)
        print("Servidor criado para a nevoa na porta:", self._nevoa_port)

    def _on_nevoa_recieve(self, client_socket: socket) -> None:
        print(f'CLOUD BEST REGION QUEUES -> {self._best_region_queues}')
        new_best_gas_station = loads(client_socket.recv(DEFAULT_RECV_TCP_BYTES).decode().replace("'", '"'))
        self._add_best_gas_station(new_best_gas_station)

    def _add_best_gas_station(self, new_best_gas_station) -> None:
        if len(self._best_region_queues) == 3:
            self._refresh_best_gas_stations(new_best_gas_station)
        else:
            new_best_gas_station_region_id = new_best_gas_station['region_id']
            best_gas_station_region_ids = list(map(lambda gas_station: gas_station['region_id'], self._best_region_queues))
            if new_best_gas_station_region_id not in best_gas_station_region_ids:
                self._best_region_queues.append(new_best_gas_station)
                self._sort_best_region_queues()
            else:
                curr_best_gas_station_id = self._best_region_queues[new_best_gas_station_region_id - 1]['id']
                curr_best_gas_station_queue = self._best_region_queues[new_best_gas_station_region_id - 1]['queue']
                if new_best_gas_station_region_id != curr_best_gas_station_id:
                    self._best_region_queues[new_best_gas_station_region_id - 1] = new_best_gas_station
                    self._sort_best_region_queues()
                elif new_best_gas_station_region_id != curr_best_gas_station_queue:
                    self._best_region_queues[new_best_gas_station_region_id - 1] = new_best_gas_station
                    self._sort_best_region_queues()

    def _refresh_best_gas_stations(self, new_best_gas_station: dict) -> None:
        new_best_gas_station_region_id = new_best_gas_station['region_id']
        new_best_gas_station_queue = new_best_gas_station['queue']
        old_best_gas_station = self._best_region_queues[new_best_gas_station_region_id - 1]
        old_best_gas_station_queue = old_best_gas_station['queue']
        if old_best_gas_station_queue != new_best_gas_station_queue:
            self._best_region_queues[new_best_gas_station_region_id - 1] = new_best_gas_station

    def _create_car_server_side(self) -> socket:
        client_socket, addr = self._socket_car.accept()
        Thread(target=self._create_car_server_side).start()
        self._on_car_recieve(client_socket)

    def _get_best_gas_station_queue(self) -> dict:
        return max(self._best_region_queues, key=lambda gas_station: gas_station['queue'])

    # Responder para o carro o melhor posto com base na regiao
    # que ele esta
    # Depois de receber a requisicao do carro eu preciso retornar
    # o melhor posto para ele.
    def _on_car_recieve(self, client_socket) -> None:
        msg = self._generate_car_response()
        client_socket.send(msg.encode(encoding='UTF-8'))
        #client_socket.close()

    def _generate_car_response(self) -> str:
        best_gas_station = self._get_best_gas_station_queue()
        best_gas_station_queue = best_gas_station['queue']
        best_gas_station_id = best_gas_station['id']
        best_gas_station_region_id = best_gas_station['region_id']
        msg = f'{{"status":"ok", "id": "{best_gas_station_id}", "queue": {best_gas_station_queue},' \
              f' "region_id": {best_gas_station_region_id}}}'
        return msg

    def _server_nevoa_on(self) -> None:
        print(f'\033[1;31;42mCLOUD BEST REGION QUEUES: -> {self._best_region_queues}\033[m')
        self._create_nevoa_server_side()


    def _server_car_on(self) -> None:
        self._create_car_server_side()
        print(f'\033[1;31mRECEIVE REQUEST FROM CAR\033[m')

    def start_cloud(self) -> None:
        self.create_server_nevoa()
        self.create_server_car()
        thread1 = Thread(target=self._server_nevoa_on)
        thread2 = Thread(target=self._server_car_on)
        thread1.start()
        thread2.start()
