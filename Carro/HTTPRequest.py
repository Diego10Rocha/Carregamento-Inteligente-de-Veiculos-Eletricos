class SimpleHttpRequest:
    def __init__(self) -> None:
        self._host: str = None
        self._port: int = None
        self._method: str = None
        self._path: str = None
        self._query_params: list = None
        self._user_agent: str = None
        self._data: dict = {}

    def get_query_params(self) -> list:
        return self._query_params

    def set_query_params(self, url: str) -> None:
        self._query_params = url

    def get_method(self) -> str:
        return self._method

    def set_method(self, method: str) -> None:
        self._method = method

    def get_user_agent(self) -> str:
        return self._user_agent

    def set_user_agent(self, user_agent: str) -> None:
        self._user_agent = user_agent

    def get_data(self) -> dict:
        return self._data

    def set_data(self, data: dict) -> None:
        self._data = data

    def get_host(self) -> str:
        return self._host

    def set_host(self, host: str) -> None:
        self._host = host

    def get_port(self) -> int:
        return self._port

    def set_port(self, port: int) -> None:
        self._port = port

    def set_path(self, path: str) -> None:
        self._path = path

    def get_path(self) -> str:
        return self._path
