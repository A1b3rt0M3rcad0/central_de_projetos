from src.infra.relational.config.interface.i_string_connection import IStringConnection
import dotenv
import os
from pathlib import Path

class StringConnection(IStringConnection):

    def __init__(self) -> None:
        env_path = Path('.') / '.env'
        dotenv.load_dotenv(dotenv_path=env_path, override=True)
        self.DATABASE = os.getenv('DATABASE')
        self.DRIVE = os.getenv('DRIVE')
        self.USERNAME = os.getenv('USERNAME')
        self.PASSWORD = os.getenv('PASSWORD')
        self.HOST = os.getenv('HOST')
        self.PORT = os.getenv('PORT')
        self.DATABASE_NAME = os.getenv('DATABASE_NAME')
        self.__valid_env_params()
        self.__connection = \
        f'{self.DATABASE}+{self.DRIVE}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE_NAME}'
    
    def get_connection(self) -> str:
        return self.__connection

    def __valid_env_params(self) -> None:
        theme = 'DATABASE-CONNECTION-ERROR:'
        if not self.DATABASE:
            raise ValueError(f'{theme} DATABASE var is empty')
        if not self.DRIVE:
            raise ValueError(f'{theme} DRIVE var is empty')
        if not self.HOST:
            raise ValueError(f'{theme} HOST var is empty')
        if not self.PORT:
            raise ValueError(f'{theme} PORT var is empty')
        if not self.DATABASE_NAME:
            raise ValueError(f'{theme} DATABASE_NAME var is empty')
