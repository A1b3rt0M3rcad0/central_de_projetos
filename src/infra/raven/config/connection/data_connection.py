import os
import dotenv
from typing import Dict
from src.infra.raven.config.connection.interface.i_data_connection import IDataConnection

class DataConnection(IDataConnection):
    def __init__(self) -> None:
        dotenv.load_dotenv()
        self.__RAVEN_URL = os.getenv("RAVEN_URL")
        self.__RAVEN_DATABASE = os.getenv("RAVEN_DATABASE")
        self.__RAVEN_CERTIFICATE_PATH = os.getenv("RAVEN_CERTIFICATE_PATH")
        self.__RAVEN_CERTIFICATE_PASSWORD = os.getenv("RAVEN_CERTIFICATE_PASSWORD")

    def data(self) -> Dict:
        if self.__RAVEN_CERTIFICATE_PATH and self.__RAVEN_CERTIFICATE_PATH.lower() != "null":
            return {
                "urls": [self.__RAVEN_URL],
                "database": self.__RAVEN_DATABASE,
                "certificate": (self.__RAVEN_CERTIFICATE_PATH, self.__RAVEN_CERTIFICATE_PASSWORD)
            }
        return {
            "urls": [self.__RAVEN_URL],
            "database": self.__RAVEN_DATABASE
        }
