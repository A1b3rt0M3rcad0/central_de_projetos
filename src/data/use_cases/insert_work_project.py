from src.domain.use_cases.i_insert_work_project import IInsertWorkProject
from src.data.interface.i_work_project_repository import IWorkProjectRepository

class InsertWorkProject(IInsertWorkProject):
    
    def __init__(self, work_project_repository:IWorkProjectRepository) -> None:
        self.__work_project_repository = work_project_repository
    
    def insert(self, project_id:int, fiscal_id:int, title:str, description:str, photo_name:str, additional_documents=None) -> int:
        return self.__work_project_repository.insert(
            project_id=project_id,
            fiscal_id=fiscal_id,
            title=title,
            description=description,
            photo_name=photo_name,
            additional_documents=additional_documents
        ) 