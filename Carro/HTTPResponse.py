class SimpleHttpResponse:
    def __init__(self) -> None:
        self._status_code: int = None
        self._data: dict = None

    def set_status_code(self, status_code: int) -> None:
        self._status_code = status_code

    def get_status_code(self) -> int:
        return self._status_code

    def set_data(self, data: dict) -> None:
        self._data = data

    def get_data(self) -> dict:
        return self._data
