from typing import Final

REGION_1: Final = 1
REGION_2: Final = 2
REGION_3: Final = 3

DEFAULT_RECV_TCP_BYTES: Final = 1024

CLOUD_ADDR: Final = '172.16.103.7'
CLOUD_CAR_PORT: Final = 1853
CLOUD_NEVOA_PORT: Final = 1873

BROKER_REGION_1_ADDR: Final = "172.16.103.3"
BROKER_REGION_1_PORT: Final = 1017

BROKER_REGION_2_ADDR: Final = "172.16.103.5"
BROKER_REGION_2_PORT: Final = 8331

BROKER_REGION_3_ADDR: Final = "172.16.103.8"
BROKER_REGION_3_PORT: Final = 1888
  
GAS_STATION_TIME_TO_SEND: Final = 7
GAS_STATION_TIME_TO_REFRESH: Final = 90
EDGE_TIME_TO_SEND: Final = 10

'''
Este arquivo define constantes relacionadas aos protrocolos
HTTP e CKINHTTP que sao utilizadas em SoftApi.py e em Medidor.py
'''

DEFAULT_TCP_BYTES: Final = 1024
MAX_TCP_BYTES: Final = 65535
HTTP_HEADER_RESPONSE: Final = 'HTTP/1.1 200 OK\r\n\r\n'
HTTP_HEADER_500_ERROR: Final = 'HTTP/1.1 500 Internal Server Error\r\n\r\n'


ACCEPT_HTTP_VERSION: Final = 1.1

# Metodos HTTP
HTTP_METHOD_GET: Final = "GET"
HTTP_METHOD_POST: Final = "POST"
HTTP_METHOD_PUT: Final = "PUT"
HTTP_METHOD_DELETE: Final = "DELETE"
INVALID_HTTP_METHOD: Final = "UNKNOW"

# Nome protocolo HTTP
HTTP_PROTOCOL: Final = "HTTP"

# Rota que guarda as faturas de todos os
# clientes
METER_TAX: Final = "faturas"

# WARNING: do not touch this if you don't have no idea what do
# Os dados vindouros dos medidores serao depositados nesta rota,
METER_API_ROUTE: Final = "clientes"
