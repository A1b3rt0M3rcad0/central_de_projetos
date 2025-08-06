from src.domain.use_cases.i_update_work_project_documents import IUpdateWorkProjectDocuments
from src.data.interface.i_work_project_repository import IWorkProjectRepository
import json

class UpdateWorkProjectDocuments(IUpdateWorkProjectDocuments):
    
    def __init__(self, work_project_repository: IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def update(self, work_project_id: int, additional_documents: str) -> None:
        if not additional_documents or len(additional_documents.strip()) == 0:
            raise ValueError("Additional documents cannot be empty")
        
        # Validar se é um JSON válido
        try:
            new_documents = json.loads(additional_documents)
        except json.JSONDecodeError as e:
            raise ValueError("Additional documents must be a valid JSON string") from e
        
        # Carregar work_project existente
        work_project = self.__work_project_repository.find(work_project_id)
        
        # Obter documentos existentes
        existing_documents = []
        if work_project.additional_documents:
            # Se já é uma lista (JSON), usar diretamente
            if isinstance(work_project.additional_documents, list):
                existing_documents = work_project.additional_documents
            else:
                # Se é string, tentar fazer parse
                try:
                    existing_documents = json.loads(work_project.additional_documents)
                except (json.JSONDecodeError, TypeError):
                    # Se não conseguir fazer parse, começa com lista vazia
                    existing_documents = []
        
        # Garantir que existing_documents seja uma lista
        if not isinstance(existing_documents, list):
            existing_documents = []
        
        # Garantir que new_documents seja uma lista
        if not isinstance(new_documents, list):
            new_documents = [new_documents]
        
        # Adicionar novos documentos à lista existente
        updated_documents = existing_documents + new_documents
        
        # Remover duplicatas mantendo a ordem
        seen = set()
        unique_documents = []
        for doc in updated_documents:
            if doc not in seen:
                seen.add(doc)
                unique_documents.append(doc)
        
        # Salvar como lista (JSON) diretamente, não como string
        self.__work_project_repository.update(
            work_project_id=work_project_id,
            update_params={"additional_documents": unique_documents}
        ) 