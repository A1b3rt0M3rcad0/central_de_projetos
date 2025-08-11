from src.domain.use_cases.i_remove_document_from_work_project import IRemoveDocumentFromWorkProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository
import json

class RemoveDocumentFromWorkProject(IRemoveDocumentFromWorkProject):
    
    def __init__(self, work_project_repository: IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def remove(self, work_project_id: int, document_name: str) -> None:
        try:
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
            
            # Remover o documento da lista
            if document_name in existing_documents:
                existing_documents.remove(document_name)
            else:
                # Se o documento não estiver na lista, não fazer nada (pode ter sido deletado anteriormente)
                pass
            
            # Salvar a lista atualizada
            self.__work_project_repository.update(
                work_project_id=work_project_id,
                update_params={"additional_documents": existing_documents}
            )
        except Exception as e:
            raise e from e 