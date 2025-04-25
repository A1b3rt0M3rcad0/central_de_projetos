from src.domain.value_objects.document import Document
from typing import List
from abc import ABC, abstractmethod

class ISaveDocument(ABC):

    @abstractmethod
    def save(self, project_id:int, document:List[Document]) -> None:
        """
        Adiciona uma lista de documentos a um projeto no banco de dados.

        Parâmetros:
            project_id: O ID do projeto ao qual os documentos serão associados.
            document: Lista de documentos a serem salvos no banco de dados.

        Levanta:
            FileSaveError (500): Caso ocorra um erro ao salvar os documentos no banco de dados.
        """