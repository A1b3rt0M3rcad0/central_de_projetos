from src.domain.value_objects.monetary_value import MonetaryValue
from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_update_project_verba import IUpdateProjectVerba

class UpdateProjectVerba(IUpdateProjectVerba):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def update(self, project_id:int, verba_disponivel:MonetaryValue) -> None:
        try:
            update_params = {'verba_disponivel': float(verba_disponivel.value)}
            self.__project_repository.update(
                project_id=project_id,
                update_params=update_params
            )
        except Exception as e:
            raise e from e