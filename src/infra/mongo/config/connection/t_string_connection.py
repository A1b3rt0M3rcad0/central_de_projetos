import os
import dotenv
from src.infra.mongo.config.connection.interface.i_string_connection import IStringConnection

class TStringConnection(IStringConnection):
    def __init__(self):
        dotenv.load_dotenv()
        self.host = os.getenv("TMONGO_HOST")
        self.port = os.getenv("TMONGO_PORT")
        self.user = os.getenv("TMONGO_USERNAME")
        self.password = os.getenv("TMONGO_PASSWORD")
        self.database = os.getenv("TMONGO_DB_NAME")
        if "null" not in (self.user, self.password):
            self.__string = f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/'
        else:
            self.__string = f'mongodb://{self.host}:{self.port}/'

    @property
    def string(self) -> str:
        return self.__string
    
    def database_name(self) -> str:
        return self.database