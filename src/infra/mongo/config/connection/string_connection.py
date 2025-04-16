import os
import dotenv
from src.infra.relational.config.interface.i_string_connection import IStringConnection

class StringConnection(IStringConnection):
    def __init__(self):
        dotenv.load_dotenv()
        self.host = os.getenv("MONGO_HOST")
        self.port = os.getenv("MONGO_PORT")
        self.user = os.getenv("MONGO_USERNAME")
        self.password = os.getenv("MONGO_PASSWORD")
        self.database = os.getenv("MONGO_DB_NAME")
        if "null" not in (self.user, self.password):
            self.__string = f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}/'
        else:
            self.__string = f'mongodb://{self.host}:{self.port}/'

    @property
    def string(self) -> str:
        return self.__string
    
    def database_name(self) -> str:
        return self.database