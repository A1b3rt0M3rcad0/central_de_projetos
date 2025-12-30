from src.domain.use_cases.i_delete_eap_from_project import IDeleteEAPFromProject
from src.data.interface.i_eap_repository import IEAPRepository

class DeleteEAPFromProject(IDeleteEAPFromProject):

    def __init__(self, eap_repository: IEAPRepository) -> None:
        self.__eap_repository = eap_repository
    
    def delete(self, project_id: int) -> None:
        try:
            self.__eap_repository.delete_by_project_id(
                project_id=project_id
            )
        except Exception as e:
            raise e from e

