#pylint:disable=W0611
from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.entities.eap import EAPEntity, EAPItemEntity
from src.data.interface.i_eap_repository import IEAPRepository
from src.data.interface.i_eap_item_repository import IEAPItemRepository
from src.domain.value_objects.eap_code import EAPCode
from src.domain.value_objects.eap_type import EAPType
from src.domain.value_objects.eap_status import EAPStatus
from src.domain.value_objects.monetary_value import MonetaryValue
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory

# Import models to ensure they are loaded
from src.infra.relational.models.eap import EAP, EAPItem
from src.infra.relational.models.project import Project
from src.infra.relational.models.user import User
from src.infra.relational.models.history_project import HistoryProject
from src.infra.relational.models.user_project import UserProject
from src.infra.relational.models.project_bairro import ProjectBairro
from src.infra.relational.models.project_empresa import ProjectEmpresa
from src.infra.relational.models.project_type import ProjectType
from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.models.status import Status
from src.infra.relational.models.bairro import Bairro
from src.infra.relational.models.empresa import Empresa
from src.infra.relational.models.fiscal import Fiscal
from src.infra.relational.models.types import Types
from src.infra.relational.models.refresh_token import RefreshToken
from src.infra.relational.models.work_project import WorkProject
from src.infra.relational.models.notification import Notification


class EAPRepository(IEAPRepository):
    """Implementação do repositório de EAP"""
    
    def __init__(self, db_connection_handler, eap_item_repository: IEAPItemRepository):
        self.__db_connection_handler = db_connection_handler
        self.__eap_item_repository = eap_item_repository
    
    def create(self, eap: EAPEntity) -> EAPEntity:
        """
        Cria uma nova EAP
        
        Args:
            eap: Entidade EAP a ser criada
            
        Returns:
            EAPEntity: A EAP criada com ID
        """
        with self.__db_connection_handler as db:
            eap_model = EAP(
                name=eap.name,
                description=eap.description,
                project_id=eap.project_id,
                is_template=eap.is_template,
                template_source_id=eap.template_source_id,
                created_by=eap.created_by,
                created_at=eap.created_at,
                updated_at=eap.updated_at
            )
            
            db.session.add(eap_model)
            db.session.commit()
            db.session.refresh(eap_model)
            
            return self._model_to_entity(eap_model)
    
    def find_by_id(self, eap_id: int) -> Optional[EAPEntity]:
        """
        Busca uma EAP pelo ID
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            EAPEntity: A EAP encontrada ou None
        """
        with self.__db_connection_handler as db:
            eap_model = db.session.query(EAP).filter(EAP.id == eap_id).first()
            
            if not eap_model:
                return None
            
            return self._model_to_entity(eap_model)
    
    def find_by_project_id(self, project_id: int) -> Optional[EAPEntity]:
        """
        Busca a EAP de um projeto específico
        
        Args:
            project_id: ID do projeto
            
        Returns:
            EAPEntity: A EAP do projeto ou None
        """
        with self.__db_connection_handler as db:
            eap_model = db.session.query(EAP).filter(
                EAP.project_id == project_id,
                EAP.is_template.is_(False)
            ).first()
            
            if not eap_model:
                return None
            
            return self._model_to_entity(eap_model)
    
    def find_templates(self) -> List[EAPEntity]:
        """
        Busca todas as EAPs que são templates
        
        Returns:
            List[EAPEntity]: Lista de EAPs templates
        """
        with self.__db_connection_handler as db:
            eap_models = db.session.query(EAP).filter(EAP.is_template.is_(True)).all()
            
            return [self._model_to_entity(model) for model in eap_models]
    
    def find_by_name(self, name: str) -> List[EAPEntity]:
        """
        Busca EAPs pelo nome (busca parcial)
        
        Args:
            name: Nome ou parte do nome da EAP
            
        Returns:
            List[EAPEntity]: Lista de EAPs encontradas
        """
        with self.__db_connection_handler as db:
            eap_models = db.session.query(EAP).filter(
                EAP.name.ilike(f"%{name}%")
            ).all()
            
            return [self._model_to_entity(model) for model in eap_models]
    
    def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[EAPEntity]:
        """
        Busca todas as EAPs com paginação
        
        Args:
            limit: Limite de resultados
            offset: Offset para paginação
            
        Returns:
            List[EAPEntity]: Lista de EAPs
        """
        with self.__db_connection_handler as db:
            query = db.session.query(EAP)
            
            if offset:
                query = query.offset(offset)
            
            if limit:
                query = query.limit(limit)
            
            eap_models = query.all()
            
            return [self._model_to_entity(model) for model in eap_models]
    
    def update(self, eap: EAPEntity) -> EAPEntity:
        """
        Atualiza uma EAP
        
        Args:
            eap: Entidade EAP com dados atualizados
            
        Returns:
            EAPEntity: A EAP atualizada
        """
        with self.__db_connection_handler as db:
            eap_model = db.session.query(EAP).filter(EAP.id == eap.id).first()
            
            if not eap_model:
                raise ValueError(f"EAP com ID {eap.id} não encontrada")
            
            eap_model.name = eap.name
            eap_model.description = eap.description
            eap_model.updated_at = eap.updated_at
            
            db.session.commit()
            db.session.refresh(eap_model)
            
            return self._model_to_entity(eap_model)
    
    def delete(self, eap_id: int) -> None:
        """
        Exclui uma EAP e todos os seus itens (exclusão em cascata)
        
        Args:
            eap_id: ID da EAP a ser excluída
        """
        with self.__db_connection_handler as db:
            eap_model = db.session.query(EAP).filter(EAP.id == eap_id).first()
            
            if not eap_model:
                raise ValueError(f"EAP com ID {eap_id} não encontrada")
            
            # Primeiro, excluir todos os itens da EAP usando o repositório de itens
            # Buscar todos os itens da EAP
            eap_items = db.session.query(EAPItem).filter(EAPItem.eap_id == eap_id).all()
            
            # Excluir todos os itens (a exclusão em cascata dos filhos já está implementada)
            for item in eap_items:
                db.session.delete(item)
            
            # Excluir a EAP
            db.session.delete(eap_model)
            db.session.commit()
    
    def count_by_project_id(self, project_id: int) -> int:
        """
        Conta quantas EAPs um projeto possui
        
        Args:
            project_id: ID do projeto
            
        Returns:
            int: Número de EAPs do projeto
        """
        with self.__db_connection_handler as db:
            return db.session.query(EAP).filter(
                EAP.project_id == project_id,
                EAP.is_template.is_(False)
            ).count()
    
    def _model_to_entity(self, eap_model: EAP) -> EAPEntity:
        """Converte um modelo SQLAlchemy para uma entidade do domínio"""
        # Busca os itens da EAP
        items = self.__eap_item_repository.find_by_eap_id(eap_model.id)
        
        return EAPEntity(
            id=eap_model.id,
            name=eap_model.name,
            description=eap_model.description,
            project_id=eap_model.project_id,
            is_template=eap_model.is_template,
            template_source_id=eap_model.template_source_id,
            created_by=eap_model.created_by,
            created_at=eap_model.created_at,
            updated_at=eap_model.updated_at,
            items=items
        )
