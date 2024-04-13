from models.d_reference import DReference

class DUser:
    def __init__(self, _id: int, login: str, password: str) -> None:
        self.id = _id
        self.login = login
        self.password = password

    def __str__(self) -> str:
        return self.name