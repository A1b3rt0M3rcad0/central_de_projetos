from abc import ABC, abstractmethod
from ravendb import DocumentSession


class IDBConnectionHandler(ABC):
    @abstractmethod
    def __enter__(self) -> DocumentSession:
        """Abre e retorna uma sessão do RavenDB"""

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Fecha a conexão com o banco de dados"""
