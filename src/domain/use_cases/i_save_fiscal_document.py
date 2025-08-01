from src.domain.value_objects.document import Document
from typing import List
from abc import ABC, abstractmethod

class ISaveFiscalDocument(ABC):

    @abstractmethod
    def save(self, project_id:int, fiscal_id:int, documents:List[Document]) -> None:
        """
        Salva documentos enviados por um fiscal específico para um projeto.

        Args:
            project_id: ID do projeto ao qual os documentos serão associados
            fiscal_id: ID do fiscal que está enviando os documentos
            documents: Lista de documentos a serem salvos

        Raises:
            FiscalDocumentSaveError (500): Caso ocorra um erro ao salvar os documentos
            FiscalNotFoundError (404): Se o fiscal não for encontrado
            ProjectNotFoundError (404): Se o projeto não for encontrado
        """