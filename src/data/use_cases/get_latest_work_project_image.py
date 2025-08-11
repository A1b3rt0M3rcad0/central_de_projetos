from src.domain.use_cases.i_get_latest_work_project_image import IGetLatestWorkProjectImage
from src.data.interface.i_project_document_fiscal_repository import IProjectDocumentFiscalRepository
from src.data.interface.i_work_project_repository import IWorkProjectRepository
import json

class GetLatestWorkProjectImage(IGetLatestWorkProjectImage):

    def __init__(self, 
                 project_document_fiscal_repository: IProjectDocumentFiscalRepository,
                 work_project_repository: IWorkProjectRepository) -> None:
        self.__project_document_fiscal_repository = project_document_fiscal_repository
        self.__work_project_repository = work_project_repository

    def get_latest_image(self, work_project_id: int) -> bytes:
        try:
            # Verificar se o work project existe
            work_project = self.__work_project_repository.find(work_project_id)
            
            # Obter documentos do work project
            additional_documents = work_project.additional_documents
            
            if not additional_documents:
                return None
            
            # Parsear a lista de documentos
            try:
                document_names = json.loads(additional_documents)
            except json.JSONDecodeError:
                return None
            
            if not document_names:
                return None
            
            # Pegar o último documento (assumindo que é uma imagem)
            latest_document_name = document_names[-1]
            
            # Verificar se é uma imagem baseada na extensão
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            if not any(latest_document_name.lower().endswith(ext) for ext in image_extensions):
                # Se não for imagem, procurar pela primeira imagem na lista
                for doc_name in reversed(document_names):
                    if any(doc_name.lower().endswith(ext) for ext in image_extensions):
                        latest_document_name = doc_name
                        break
                else:
                    return None
            
            # Buscar a imagem no repositório de documentos fiscais
            # Como não temos fiscal_id específico, vamos buscar por work_project_id
            # Assumindo que o repositório pode buscar por work_project_id
            try:
                image_data = self.__project_document_fiscal_repository.get_document_by_work_project_and_name(
                    work_project_id=work_project_id,
                    document_name=latest_document_name
                )
                return image_data
            except Exception:
                return None
                
        except Exception as e:
            raise e from e 