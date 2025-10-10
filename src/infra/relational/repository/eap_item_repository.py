#pylint:disable=W0611
from typing import List, Optional
from sqlalchemy.orm import Session

from src.domain.entities.eap import EAPItemEntity
from src.data.interface.i_eap_item_repository import IEAPItemRepository
from src.domain.value_objects.eap_code import EAPCode
from src.domain.value_objects.eap_type import EAPType
from src.domain.value_objects.eap_status import EAPStatus
from src.domain.value_objects.monetary_value import MonetaryValue
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory

# Import models to ensure they are loaded
from src.infra.relational.models.eap import EAPItem, EAP


class EAPItemRepository(IEAPItemRepository):
    """Implementação do repositório de itens da EAP"""
    
    def __init__(self, db_connection_handler):
        self.__db_connection_handler = db_connection_handler
    
    def create(self, item: EAPItemEntity) -> EAPItemEntity:
        """
        Cria um novo item da EAP
        
        Args:
            item: Entidade EAPItem a ser criada
            
        Returns:
            EAPItemEntity: O item criado com ID
        """
        with self.__db_connection_handler as db:
            item_model = EAPItem(
                eap_id=item.eap_id,
                code=str(item.code),
                name=item.name,
                description=item.description,
                type=item.type.value,
                parent_id=item.parent_id,
                responsible=item.responsible,
                start_date=item.start_date,
                end_date=item.end_date,
                budget=float(item.budget.value),
                status=item.status.value,
                progress=item.progress,
                created_at=item.created_at,
                updated_at=item.updated_at
            )
            
            db.session.add(item_model)
            db.session.commit()
            db.session.refresh(item_model)
            
            return self._model_to_entity(item_model)
    
    def find_by_id(self, item_id: int) -> Optional[EAPItemEntity]:
        """
        Busca um item pelo ID
        
        Args:
            item_id: ID do item
            
        Returns:
            EAPItemEntity: O item encontrado ou None
        """
        with self.__db_connection_handler as db:
            item_model = db.session.query(EAPItem).filter(EAPItem.id == item_id).first()
            
            if not item_model:
                return None
            
            return self._model_to_entity(item_model)
    
    def find_by_eap_id(self, eap_id: int) -> List[EAPItemEntity]:
        """
        Busca todos os itens de uma EAP
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            List[EAPItemEntity]: Lista de itens da EAP
        """
        with self.__db_connection_handler as db:
            item_models = db.session.query(EAPItem).filter(EAPItem.eap_id == eap_id).all()
            
            return [self._model_to_entity(model) for model in item_models]
    
    def find_by_parent_id(self, parent_id: int) -> List[EAPItemEntity]:
        """
        Busca todos os itens filhos de um item específico
        
        Args:
            parent_id: ID do item pai
            
        Returns:
            List[EAPItemEntity]: Lista de itens filhos
        """
        with self.__db_connection_handler as db:
            item_models = db.session.query(EAPItem).filter(EAPItem.parent_id == parent_id).all()
            
            return [self._model_to_entity(model) for model in item_models]
    
    def find_root_items(self, eap_id: int) -> List[EAPItemEntity]:
        """
        Busca todos os itens raiz de uma EAP
        
        Args:
            eap_id: ID da EAP
            
        Returns:
            List[EAPItemEntity]: Lista de itens raiz
        """
        with self.__db_connection_handler as db:
            item_models = db.session.query(EAPItem).filter(
                EAPItem.eap_id == eap_id,
                EAPItem.parent_id.is_(None)
            ).all()
            
            return [self._model_to_entity(model) for model in item_models]
    
    def find_by_type(self, eap_id: int, eap_type: EAPType) -> List[EAPItemEntity]:
        """
        Busca todos os itens de um tipo específico em uma EAP
        
        Args:
            eap_id: ID da EAP
            eap_type: Tipo dos itens
            
        Returns:
            List[EAPItemEntity]: Lista de itens do tipo especificado
        """
        with self.__db_connection_handler as db:
            item_models = db.session.query(EAPItem).filter(
                EAPItem.eap_id == eap_id,
                EAPItem.type == eap_type.value
            ).all()
            
            return [self._model_to_entity(model) for model in item_models]
    
    def find_by_status(self, eap_id: int, status: EAPStatus) -> List[EAPItemEntity]:
        """
        Busca todos os itens com um status específico em uma EAP
        
        Args:
            eap_id: ID da EAP
            status: Status dos itens
            
        Returns:
            List[EAPItemEntity]: Lista de itens com o status especificado
        """
        with self.__db_connection_handler as db:
            item_models = db.session.query(EAPItem).filter(
                EAPItem.eap_id == eap_id,
                EAPItem.status == status.value
            ).all()
            
            return [self._model_to_entity(model) for model in item_models]
    
    def find_by_code(self, eap_id: int, code: str) -> Optional[EAPItemEntity]:
        """
        Busca um item pelo código em uma EAP específica
        
        Args:
            eap_id: ID da EAP
            code: Código do item
            
        Returns:
            EAPItemEntity: O item encontrado ou None
        """
        with self.__db_connection_handler as db:
            item_model = db.session.query(EAPItem).filter(
                EAPItem.eap_id == eap_id,
                EAPItem.code == code
            ).first()
            
            if not item_model:
                return None
            
            return self._model_to_entity(item_model)
    
    def update(self, item: EAPItemEntity) -> EAPItemEntity:
        """
        Atualiza um item da EAP
        
        Args:
            item: Entidade EAPItem com dados atualizados
            
        Returns:
            EAPItemEntity: O item atualizado
        """
        with self.__db_connection_handler as db:
            item_model = db.session.query(EAPItem).filter(EAPItem.id == item.id).first()
            
            if not item_model:
                raise ValueError(f"Item da EAP com ID {item.id} não encontrado")
            
            item_model.name = item.name
            item_model.description = item.description
            item_model.responsible = item.responsible
            item_model.start_date = item.start_date
            item_model.end_date = item.end_date
            item_model.budget = float(item.budget.value)
            item_model.status = item.status.value
            item_model.progress = item.progress
            item_model.updated_at = item.updated_at
            
            db.session.commit()
            db.session.refresh(item_model)
            
            return self._model_to_entity(item_model)
    
    def delete(self, item_id: int) -> None:
        """
        Exclui um item da EAP e todos os seus filhos (exclusão em cascata)
        
        Args:
            item_id: ID do item a ser excluído
        """
        with self.__db_connection_handler as db:
            item_model = db.session.query(EAPItem).filter(EAPItem.id == item_id).first()
            
            if not item_model:
                raise ValueError(f"Item da EAP com ID {item_id} não encontrado")
            
            # Função recursiva para excluir todos os filhos
            def delete_children(parent_id: int):
                children = db.session.query(EAPItem).filter(EAPItem.parent_id == parent_id).all()
                for child in children:
                    # Excluir recursivamente os filhos do filho
                    delete_children(child.id)
                    # Excluir o filho
                    db.session.delete(child)
            
            # Excluir todos os filhos primeiro
            delete_children(item_id)
            
            # Excluir o item principal
            db.session.delete(item_model)
            db.session.commit()
    
    def count_children(self, parent_id: int) -> int:
        """
        Conta quantos filhos um item possui
        
        Args:
            parent_id: ID do item pai
            
        Returns:
            int: Número de filhos
        """
        with self.__db_connection_handler as db:
            return db.session.query(EAPItem).filter(EAPItem.parent_id == parent_id).count()
    
    def get_children_budget_total(self, parent_id: int) -> float:
        """
        Calcula o orçamento total de todos os filhos de um item
        
        Args:
            parent_id: ID do item pai
            
        Returns:
            float: Soma do orçamento de todos os filhos
        """
        with self.__db_connection_handler as db:
            children = db.session.query(EAPItem).filter(EAPItem.parent_id == parent_id).all()
            return sum(float(child.budget) for child in children)
    
    def exists_by_code(self, eap_id: int, code: str) -> bool:
        """
        Verifica se um código já existe em uma EAP
        
        Args:
            eap_id: ID da EAP
            code: Código a ser verificado
            
        Returns:
            bool: True se o código existir
        """
        with self.__db_connection_handler as db:
            return db.session.query(EAPItem).filter(
                EAPItem.eap_id == eap_id,
                EAPItem.code == code
            ).first() is not None
    
    def _model_to_entity(self, item_model: EAPItem) -> EAPItemEntity:
        """Converte um modelo SQLAlchemy para uma entidade do domínio"""
        return EAPItemEntity(
            id=item_model.id,
            eap_id=item_model.eap_id,
            code=EAPCode(item_model.code),
            name=item_model.name,
            description=item_model.description,
            type=EAPType(item_model.type),
            parent_id=item_model.parent_id,
            responsible=item_model.responsible,
            start_date=item_model.start_date,
            end_date=item_model.end_date,
            budget=MonetaryValue(float(item_model.budget)),
            status=EAPStatus(item_model.status),
            progress=item_model.progress,
            created_at=item_model.created_at,
            updated_at=item_model.updated_at
        )
