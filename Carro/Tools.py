import consts
import HttpHeaderParser
from json import dumps
from re import findall
from os import system

'''
Arquivo que contem funcoes que lidam com parsing em
cabecalhos HTTP e CKINHTTP, calculos
de media geometrica e data e hora
'''


# Valida uma rota a ser cadastrada
# route -> Rota a ser validada
# True caso a rota seja valida e False caso contrario
def isvalidroute(route: str) -> bool:
    lst_new_route = route.split('/')
    raw_route = ''.join(lst_new_route)
    if not raw_route or not raw_route.isidentifier():
        return False
    return True


# Identifica o metodo do cabecalho de uma requisicao HTTP
# http_header -> informacao a ser parseada
# Devolve o metodo HTTP em forma de string
def http_method_type(http_header: str) -> str:
    return http_header.split('\r')[0].split(' ')[0]


# Identifica o tipo de uma requisicao, HTTP ou CKINHTTP
# request_header -> cabecalho de requisicao a ser analisado
# Devolve CKINHTTP ou HTTP, em forma de string
def request_type(request_header: str) -> str:
    if consts.HTTP_PROTOCOL in request_header.split('\n')[0]:
        return consts.HTTP_PROTOCOL
    return 'NULL'


# Identifica o tipo de requisicao
# header -> cabecalho de requisicao
# Devolve SimpleHttpRequest ou SimpleCKINHTTPRequest
def get_request_obj(header: str) -> object:
    if request_type(header) == consts.HTTP_PROTOCOL:
        return HttpHeaderParser.http_header_parser(header)
    return HttpHeaderParser.http_header_parser(header)


# Verifica a existencia de uma chave em um determinado dicionario
# dic -> dicionario
# key -> chave a ser verificada
# True caso a chave exista
# False caso a chave nao exista
def exists_uuid(dic: dict, key: str) -> bool:
    return bool(dic.get(key))


# Formata dicionario para um json em formato HTTP
# raw_json -> Dicionario a ser convertido
# Devolve o dicionario formatado em forma de string
def format_http_json(raw_json: dict) -> str:
    s_json = dumps(raw_json)
    pattern = r'"\d+-\d+-\d+\s\d+\d-\d+-\d+":\s"\d+"'
    json_data = findall(pattern, s_json)
    http_json = '{\n\t'
    if json_data:
        for i in range(len(json_data) - 1):
            http_json += json_data[i] + ',\n\t'
        http_json += json_data[-1] + '\n}'
        return http_json
    return http_json + '\n}'


# Possui a mesma funcinalidade de format_http_json
# porem para um dicionario com apenas um elemento
def r_format_http_json(raw_json: dict) -> str:
    s_json = dumps(raw_json)
    return '{\n\t"all": ' + s_json + '\n}'


# Cria um cabecalho de requisicao HTTP
# method -> metodo http
# path -> caminho da requisicao
# query -> parametros query
# user_agent -> user-agent
# Devolve o cabecalho em forma de string
def make_http_request_header(method: str, path: str = '/', query: str = '', user_agent: str = 'P1_Redes/2023.1') -> str:
    full_path = path + query
    order_line = method + ' ' + full_path + ' HTTP/1.1\r\n'
    host = 'Host: localhost:8080\r\n'
    user_agent = 'User-Agent: ' + user_agent + '\r\n\r\n'
    http_header = order_line + host + user_agent
    return http_header


# Limpa o terminal
def clear_scr() -> None:
    system('clear')
