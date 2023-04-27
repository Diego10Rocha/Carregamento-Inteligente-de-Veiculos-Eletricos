from json import loads
from typing import List, Any

from HTTPRequest import SimpleHttpRequest
from HTTPResponse import SimpleHttpResponse


# Faz o parsing em um cabecalho de uma requisicao HTTP request
# de qualquer metodo
# http_header -> cabecalho da requisicao
# Devolve um objeto que representa uma requisicao HTTP
def http_header_parser(http_header: str) -> SimpleHttpRequest:
    simpleHttpRequest = SimpleHttpRequest()
    sliced_header = slice_header(http_header)
    print("SLICED HEADER")
    print(len(sliced_header))
    method, path = get_order_line_elements(sliced_header[0])
    simpleHttpRequest.set_method(method)
    resource, query_params = _get_path_elements(path)
    simpleHttpRequest.set_path(resource)
    simpleHttpRequest.set_query_params(query_params)
    for i in range(1, len(sliced_header[1:])):
        if ishost(sliced_header[i]):
            addr, port = sliced_header[i][6:].split(':')
            simpleHttpRequest.set_host(addr)
            simpleHttpRequest.set_port(port)
        elif isuseragent(sliced_header[i]):
            simpleHttpRequest.set_user_agent(sliced_header[i][12:])
        elif isdata(sliced_header[i]):
            simpleHttpRequest.set_data(loads(sliced_header[i]))
    print("SLICED HEADER")
    print(sliced_header)
    return simpleHttpRequest


# Divide um cabecalho HTTP e remove os seus caracteres especiais
# http_header -> cabecalho de requisicao
# Devolve uma lista. Cada item da lista corresponde a uma secao do cabecalho
def slice_header(http_header: str) -> list[Any]:
    return list(map(lambda headers: headers.replace('\n', ''), http_header.split('\r')))


# Devolve os elementos da "linha de ordem" de um cabecalho HTTP
# em forma de tupla
# order_line -> linha de ordem
def get_order_line_elements(order_line: str) -> tuple:
    order_elements = order_line.split(' ')
    return order_elements[0], order_elements[1]


# Retorna os elementos do path [query params e resources]
# de uma requisicao HTTP em forma de tupla
# path -> path
def _get_path_elements(path: str) -> tuple:
    elements = path
    if path.find('?') > 0:
        elements = path.split('?')
        return elements[0][1:], elements[1]
    return path[1:], ''


# Verifica se uma string e um cabecalho Host HTTP
# header -> string a ser verificada
# Devolve true caso seja um host e false caso contrario
def ishost(header: str) -> bool:
    return bool(header.startswith("Host"))


# Verifica se uma string e um cabecalho User-Agent HTTP
# header -> string a ser verificada
# Devolve true caso seja um User-Agent e false caso contrario
def isuseragent(header: str) -> bool:
    return bool(header.startswith("User-Agent"))


# Verifica se uma string e uma secao de dados de uma requisicao HTTP
# header -> string a ser verificada
# Devolve true caso seja uma secao de dados e False caso contrario
def isdata(header: str) -> bool:
    return bool(header.startswith("{") and header.endswith("}"))


# Realiza o parsing em uma requisicao Response HTTP
# response_header -> cabecalho de uma requisicao de resposta
# Devolve um objeto que representa uma requisicao de resposta simples
def http_response_header_parser(response_header: str) -> SimpleHttpResponse:
    http_response = SimpleHttpResponse()
    sliced_header = response_header.split('\r')
    http_response.set_status_code(int(sliced_header[0].split(' ')[1]))
    http_response.set_data(loads(sliced_header[2]))
    return http_response
