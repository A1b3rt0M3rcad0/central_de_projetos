from src.data.interface.i_project_repository import IProjectRepository
from src.domain.use_cases.i_create_project import ICreateProject
from src.domain.value_objects.monetary_value import MonetaryValue
from src.errors.http.http_internal_server_error import InternalServerError
from datetime import datetime
from typing import Optional

class CreateProject(ICreateProject):

    def __init__(self, project_repository:IProjectRepository) -> None:
        self.__project_repository = project_repository
    
    def create(self, 
               status_id:int, 
               name:str, 
               verba_disponivel:Optional[MonetaryValue]=None, 
               andamento_do_projeto:Optional[str]=None, 
               start_date:Optional[datetime]=None, 
               expected_completion_date:Optional[datetime]=None, 
               end_date:Optional[datetime]=None
    ) -> None:
        try:
            self.__project_repository.insert(
                status_id=status_id,
                name=name,
                verba_disponivel=verba_disponivel,
                andamento_do_projeto=andamento_do_projeto,
                start_date=start_date,
                expected_completion_date=expected_completion_date,
                end_date=end_date
            )
        except Exception as e:
            raise InternalServerError(
                title='CreateProjectError',
                message=f'Error on create project: {e}'
            ) from e