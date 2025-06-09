from src.data.interface.i_user_project_repository import IUserProjectRepository
from src.domain.value_objects.cpf import CPF
from src.domain.value_objects.email import Email
from src.domain.entities.user_project import UserProjectEntity
from src.domain.entities.user import UserEntity
from src.infra.relational.config.interface.i_db_connection_handler import IDBConnectionHandler
from src.infra.relational.models.user_project import UserProject
from src.infra.relational.models.user import User
from sqlalchemy import and_
from typing import Optional, List, Dict

# Errors
from src.errors.repository.already_exists_error.user_project_already_exists import UserProjectAlreadyExists
from src.errors.repository.already_exists_error.user_project_not_exists import UserProjectNotExists
from src.errors.repository.error_on_insert.error_on_insert_user_project import ErrorOnInsertUserProject
from src.errors.repository.error_on_find.error_on_find_user_project import ErrorOnFindUserProject
from src.errors.repository.error_on_update.error_on_update_user_project import ErrorOnUpdateUserProject
from src.errors.repository.has_related_children.user_project_has_related_children import UserProjectHasRelatedChildren
from src.errors.repository.error_on_delete.error_on_delete_user_project import ErrorOnDeleteUserProject
from sqlalchemy.exc import IntegrityError

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
            except IntegrityError as e:
                raise UserProjectAlreadyExists(message=f'The registry with this keys: cpf: {cpf_user.value} and project_id:{project_id} already exists') from e
            except Exception as e:
                raise ErrorOnInsertUserProject(
                    message=f'Error on inser user_project user_cpf={cpf_user.value}, project_id={project_id}: {str(e)}'
                ) from e

    def find(self, cpf_user:CPF, project_id:int) -> UserProjectEntity:
        with self.__db_connection_handler as db:
            try:
                user_project = db.session.query(UserProject).where(
                    and_(
                        UserProject.user_cpf == cpf_user.value,
                        UserProject.project_id == project_id
                    )
                ).first()
                if not user_project:
                    raise UserProjectNotExists(message=f'The user project: "{(cpf_user, project_id)}" not exists')
                return UserProjectEntity(
                    cpf=user_project.user_cpf,
                    project_id=user_project.project_id,
                    data_atribuicao=user_project.assignment_date
                )
            except UserProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindUserProject(
                    message=f'Error on find user_project user_cpf={cpf_user.value}, project_id={project_id}: {str(e)}'
                ) from e
            
    def find_all_from_cpf(self, cpf_user:CPF) -> List[UserProjectEntity]:
        with self.__db_connection_handler as db:
            try:
                user_projects = db.session.query(UserProject).where(
                    UserProject.user_cpf == cpf_user.value,
                ).all()
                if not any(user_projects):
                    raise UserProjectNotExists(
                        message=f'user_project from cpf={cpf_user.value} not exists'
                    )
                relations = [
                    UserProjectEntity(
                        cpf=relation.user_cpf,
                        project_id=relation.project_id,
                        data_atribuicao=relation.assignment_date
                    ) for relation in user_projects
                ]
                return relations
            except UserProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindUserProject(
                    message=f'Error on find all user_project from cpf user_cpf={cpf_user.value}: {str(e)}'
                ) from e
    
    def find_user_by_project_id(self, project_id:int) -> UserEntity | None:
        with self.__db_connection_handler as db:
            try:
                user_project:UserProject = db.session.query(UserProject).where(UserProject.project_id == project_id).first()

                if user_project is None:
                    return None

                user:User = db.session.query(User).where(User.cpf == user_project.user_cpf).first()

                if user is not None:
                    return UserEntity(
                        cpf=CPF(user.cpf),
                        created_at=user.created_at,
                        email=Email(user.email),
                        name=user.name,
                        password=user.password,
                        role=user.role,
                        salt=user.salt,
                    )
                return None
            except Exception as e: 
                raise ErrorOnFindUserProject(
                message=f"Error on find User By Project Id: {e}"
            ) from e
    
    def find_all(self) -> List[Optional[UserProjectEntity]]:
        with self.__db_connection_handler as db:
            try:
                user_projects = db.session.query(UserProject).all()
                if not any(user_projects):
                    raise UserProjectNotExists(
                        message='user_projects not exists'
                    )
                relations = [
                    UserProjectEntity(
                        cpf=relation.user_cpf,
                        project_id=relation.project_id,
                        data_atribuicao=relation.assignment_date
                    ) for relation in user_projects
                ]
                return relations
            except UserProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnFindUserProject(
                    message=f'Error on find all user_projects: {str(e)}'
                ) from e
    
    def update(self, cpf_user:CPF, project_id:int, update_params:Dict) -> None:
        with self.__db_connection_handler as db:
            try:
                user_project = db.session.query(UserProject).where(and_(
                    UserProject.user_cpf == cpf_user.value,
                    UserProject.project_id == project_id
                )).all()
                if not any(user_project):
                    raise UserProjectNotExists(
                        message=f'User_project cpf_user={cpf_user.value}, project_id={project_id} not exists'
                    )
                db.session.query(UserProject).where(and_(
                    UserProject.user_cpf == cpf_user.value,
                    UserProject.project_id == project_id
                )).update(update_params)
                db.session.commit()
            except UserProjectNotExists as e:
                raise e from e
            except Exception as e:
                raise ErrorOnUpdateUserProject(
                    message=f'Error on update user project cpf_user={cpf_user.value}, project_id={project_id} params={update_params}: {str(e)}'
                ) from e
    
    def delete(self, cpf_user:CPF, project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(UserProject).where(and_(
                    UserProject.user_cpf == cpf_user.value,
                    UserProject.project_id == project_id
                )).delete()
                db.session.commit()
            except IntegrityError as e:
                raise UserProjectHasRelatedChildren(
                    message=f'Error on delete user_project cpf_user={cpf_user}, project_id={project_id} because has related children: {str(e)}'
                ) from e
            except Exception as e:
                raise ErrorOnDeleteUserProject(
                    message=f'Error on delete user_project cpf_user={cpf_user}, project_id={project_id}: {str(e)}'
                ) from e
    
    def delete_all_from_project(self, project_id:int) -> None:
        with self.__db_connection_handler as db:
            try:
                db.session.query(UserProject).where(
                    UserProject.project_id == project_id
                ).delete()
                db.session.commit()
            except IntegrityError as e:
                raise UserProjectHasRelatedChildren(
                    message=f'Error on delete user_project from project project_id={project_id} because has related children: {str(e)}'
                ) from e
            except Exception as e:
                raise ErrorOnDeleteUserProject(
                    message=f'Error on delete user_project from project project_id={project_id}: {str(e)}'
                ) from e