from src.domain.use_cases.i_create_project_folder import ICreateProjectFolder
from src.data.interface.i_project_folder_repository import IProjectFolderRepository

class CreateProjectFolder(ICreateProjectFolder):

    def __init__(self, project_folder_repository: IProjectFolderRepository) -> None:
        self.__project_folder_repository = project_folder_repository
    
    def create(self, project_id: int, folder_id: int) -> None:
        try:
            # Garantir que o projeto tenha apenas uma pasta: deletar todas as associações existentes
            # antes de criar a nova
            self.__project_folder_repository.delete_all_from_project(project_id=project_id)
            
            # Criar a nova associação
            self.__project_folder_repository.insert(
                project_id=project_id,
                folder_id=folder_id
            )
        except Exception as e:
            raise e from e

