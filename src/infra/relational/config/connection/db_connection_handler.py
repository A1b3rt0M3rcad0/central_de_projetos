from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy import Engine
from src.infra.relational.config.interface.i_string_connection import IStringConnection
from typing import Self

class DBConnectionHandler(IDBConnectionHandler):


    def __init__(self, connection:IStringConnection) -> None:
        self.connection = connection
        self.__engine = self.__create_engine()
        self.__session = None
    
    @property
    def session(self) -> Session:
        return self.__session
    
    def __create_engine(self) -> Engine:
        return create_engine(
            self.connection.get_connection(),
            # Pool de conexões
            pool_size=10,           # 10 conexões sempre ativas
            max_overflow=20,        # +20 conexões se necessário
            pool_pre_ping=True,     # Verifica se conexão ainda é válida
            pool_recycle=3600,      # Recicla conexões a cada 1h
            # Timeouts
            pool_timeout=30,        # Espera 30s por conexão disponível
            connect_args={
                "connect_timeout": 10,
                "read_timeout": 30
            }
        )
    
    def get_engine(self) -> Engine:
        return self.__engine
    
    def __enter__(self) -> Self:
        session_make = sessionmaker(self.__engine, expire_on_commit=False, class_=Session)
        self.__session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()