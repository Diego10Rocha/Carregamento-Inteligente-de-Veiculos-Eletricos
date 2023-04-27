import consts
from socket import socket, AF_INET, SOCK_STREAM
import Tools
import HttpHeaderParser
import HTTPRequest
import threading
from Carro import Car
from json import loads

'''
Classe que representa uma API utilizada em uma rede IOT
de medidores. Capaz de lidar com conexoes simultaneas
e que se comporta como REST e não-rest.
Alem de conexoes HTTP a API lida com requisicoes CKINHTTP
'''


class SoftAPI:
    def __init__(self, addr: str, port: int, region_id: int) -> None:
        self._addr: str = addr
        self._port: int = port
        self._socket: socket = None
        self._routes: dict = dict()
        self._raw_api_controller: Car = Car(region_id)

    # Instancia um socket TCP do tipo server
    def create_server(self) -> None:
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.bind((self._addr, self._port))
        self._socket.listen()

    # Torna disponível a API 
    def server_on(self) -> None:
        print("listening on", self._port)
        client_socket, addr = self._socket.accept()
        print("someone connect")
        threading.Thread(target=self.server_on).start()
        client_request = client_socket.recv(consts.DEFAULT_TCP_BYTES).decode()
        return self.response_http(HttpHeaderParser.http_header_parser(client_request), client_socket)

    # Cria uma rota que suporta o metodo HTTP GET
    # new_route -> rota a ser criada
    # controller -> controller da rota
    def create_get(self, new_route: str) -> None:
        self._routes[new_route] = [consts.HTTP_METHOD_GET]

    # Responde uma requisicao HTTP de forma adequada
    # http_request -> requisicao HTTP
    # client_socket -> conexao do cliente
    def response_http(self, http_request: HTTPRequest.SimpleHttpRequest, client_socket: socket) -> None:
        http_method = http_request.get_method()
        path = http_request.get_path()
        if http_method in self._supported_http_methods(path):
            match http_method:
                case consts.HTTP_METHOD_GET:
                    return self._response_http_get(http_request, client_socket)
                case consts.HTTP_METHOD_POST:
                    client_socket.send(consts.HTTP_HEADER_500_ERROR.encode())
                    return
                case consts.HTTP_METHOD_PUT:
                    client_socket.send(consts.HTTP_HEADER_500_ERROR.encode())
                    return
                case consts.HTTP_METHOD_DELETE:
                    client_socket.send(consts.HTTP_HEADER_500_ERROR.encode())
                    return

    # Retornatodos os metodos que determinada rota suporta
    # route -> rota a ser verificada
    def _supported_http_methods(self, route: str) -> list:
        print(self._routes[route][0])
        return self._routes[route][0]

    # Responde uma requisicao HTTP GET de forma adequada
    # http_request -> requisicao HTTP GET
    # client_socket -> conexao do cliente
    def _response_http_get(self, http_request: HTTPRequest.SimpleHttpRequest, client_socket: socket) -> None:
        route = http_request.get_path()
        print(route)
        print(self._raw_api_controller.recharging)
        if route == "posto" or route == '/posto':
            car = self._raw_api_controller
            if car.recharging:
                msg = loads(f'{{"message": "Recharging on region id {car.best_station.region} over gas_station id '
                            f'{car.best_station.id}"}}')
            else:
                msg = loads(f'{{"message": "Recharging {car.battery_level} % battery"}}')
            response_json = Tools.r_format_http_json(msg)
            client_socket.send((consts.HTTP_HEADER_RESPONSE + response_json).encode())
        else:
            client_socket.send(consts.HTTP_HEADER_500_ERROR.encode())
