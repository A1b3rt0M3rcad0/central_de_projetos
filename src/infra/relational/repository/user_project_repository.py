from src.data.interface.i_user_project_repository import IUserProjectRepository
from src.domain.value_objects.cpf import CPF
from src.domain.entities.user_project import UserProjectEntity
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.relational.models.user_project import UserProject
from sqlalchemy import and_
from typing import Optional, List, Dict

class UserProjectRepository(IUserProjectRepository):
    
    def __init__(self, db_connection_handler:IDBConnectionHandler) -> None:
        self.__db_connection_handler = db_connection_handler
    
    def insert(self, cpf_user:CPF, project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.add(
                    UserProject(
                        user_cpf=cpf_user.value,
                        project_id=project_id
                    )
                )
                db.session.commit()
            except Exception as e:
                raise e

    def find(self, cpf_user:CPF, project_id:int) -> UserProjectEntity:
        with self.__db_connection_handler as db:
            try:
                user_project = db.session.query(UserProject).where(
                    and_(
                        UserProject.user_cpf == cpf_user.value,
                        UserProject.project_id == project_id
                    )
                ).first()
                return UserProjectEntity(
                    cpf=user_project.user_cpf,
                    project_id=user_project.project_id,
                    data_atribuicao=user_project.assignment_date
                )
            except Exception as e:
                raise e
    
    def find_all(self) -> List[Optional[UserProjectEntity]]:
        with self.__db_connection_handler as db:
            try:
                user_projects = db.session.query(UserProject).all()
                relations = [
                    UserProjectEntity(
                        cpf=relation.user_cpf,
                        project_id=relation.project_id,
                        data_atribuicao=relation.assignment_date
                    ) for relation in user_projects
                ]
                return relations
            except Exception as e:
                raise e
    
    def update(self, cpf_user:CPF, project_id:int, update_params:Dict) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(UserProject).where(and_(
                    UserProject.user_cpf == cpf_user.value,
                    UserProject.project_id == project_id
                )).update(update_params)
                db.session.commit()
            except Exception as e:
                raise e
    
    def delete(self, cpf_user:CPF, project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(UserProject).where(and_(
                    UserProject.user_cpf == cpf_user.value,
                    UserProject.project_id == project_id
                )).delete()
                db.session.commit()
            except Exception as e:
                raise e