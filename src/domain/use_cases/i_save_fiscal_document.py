from src.domain.value_objects.document import Document
from typing import List
from abc import ABC, abstractmethod

class ISaveFiscalDocument(ABC):

    @abstractmethod
    def save(self, work_project_id:int, fiscal_id:int, documents:List[Document]) -> None:
        """
        Salva documentos enviados por um fiscal específico para um work project.

        Args:
            work_project_id: ID do work project ao qual os documentos serão associados
            fiscal_id: ID do fiscal que está enviando os documentos
            documents: Lista de documentos a serem salvos

        Raises:
            FiscalDocumentSaveError (500): Caso ocorra um erro ao salvar os documentos
            FiscalNotFoundError (404): Se o fiscal não for encontrado
            WorkProjectNotFoundError (404): Se o work project não for encontrado
        """