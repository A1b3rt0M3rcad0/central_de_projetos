import os
import dotenv
from src.infra.relational.config.interface.i_string_connection import IStringConnection

class StringConnection(IStringConnection):
    def __init__(self):
        dotenv.load_dotenv()
        self.host = os.getenv("TMONGO_HOST")
        self.port = os.getenv("TMONGO_PORT")
        self.user = os.getenv("TMONGO_USER")
        self.password = os.getenv("TMONGO_PASSWORD")
        self.database = os.getenv("TMONGO_DB_NAME")
        if "null" not in (self.user, self.password):
            self.__string = f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}'
        else:
            self.__string = f'mongodb://{self.host}:{self.port}'

    @property
    def string(self) -> str:
        return self.__string