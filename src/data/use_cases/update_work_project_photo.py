from src.domain.use_cases.i_update_work_project_photo import IUpdateWorkProjectPhoto
from src.data.interface.i_work_project_repository import IWorkProjectRepository
from src.errors.use_cases.photo_not_in_documents_error import PhotoNotInDocumentsError
import json

class UpdateWorkProjectPhoto(IUpdateWorkProjectPhoto):
    
    def __init__(self, work_project_repository: IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def update(self, work_project_id: int, photo_name: str) -> None:
        if not photo_name or len(photo_name.strip()) == 0:
            raise ValueError("Photo name cannot be empty")
        
        # Remover espaços em branco primeiro
        photo_name_clean = photo_name.strip()
        
        # Validar extensão do arquivo - apenas imagens permitidas
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        file_extension = photo_name_clean.lower()
        if not any(file_extension.endswith(ext) for ext in allowed_extensions):
            raise ValueError(f"Invalid file extension. Only image files are allowed: {', '.join(allowed_extensions)}")
        
        # Carregar work_project existente
        work_project = self.__work_project_repository.find(work_project_id)
        
        # Verificar se a foto existe nos additional_documents
        if work_project.additional_documents:
            # Se já é uma lista (JSON), usar diretamente
            if isinstance(work_project.additional_documents, list):
                documents = work_project.additional_documents
            else:
                # Se é string, tentar fazer parse
                try:
                    documents = json.loads(work_project.additional_documents)
                    if not isinstance(documents, list):
                        documents = []
                except (json.JSONDecodeError, TypeError):
                    documents = []
        else:
            documents = []
        
        # Verificar se a foto existe na lista de documentos
        if photo_name_clean not in documents:
            raise PhotoNotInDocumentsError(photo_name_clean)
        
        self.__work_project_repository.update(
            work_project_id=work_project_id,
            update_params={"photo_name": photo_name_clean}
        ) 