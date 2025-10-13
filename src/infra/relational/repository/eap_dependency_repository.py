"""Implementação do repositório de dependências da EAP"""
#pylint:disable=W0611
from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import selectinload

from src.data.interface.i_eap_dependency_repository import IEAPDependencyRepository
from src.domain.entities.eap_dependency import EAPDependencyEntity
from src.domain.value_objects.dependency_type import DependencyType
from src.main.config.database.db_connection_handler_factory import db_connection_handler_factory

# Import models
from src.infra.relational.models.eap_item_dependency import EAPItemDependency
from src.infra.relational.models.eap import EAPItem, EAP


class EAPDependencyRepository(IEAPDependencyRepository):
    """Implementação do repositório de dependências entre itens da EAP"""
    
    def __init__(self, db_connection_handler):
        self.__db_connection_handler = db_connection_handler
    
    def create(self, dependency: EAPDependencyEntity) -> EAPDependencyEntity:
        """Cria uma nova dependência"""
        with self.__db_connection_handler as db:
            new_dep = EAPItemDependency(
                successor_id=dependency.successor_id,
                predecessor_id=dependency.predecessor_id,
                dependency_type=dependency.dependency_type.value,
                lag_days=dependency.lag_days
            )
            
            db.session.add(new_dep)
            db.session.commit()
            db.session.refresh(new_dep)
            
            return self._to_entity(new_dep)
    
    def find_by_id(self, dependency_id: int) -> Optional[EAPDependencyEntity]:
        """Busca uma dependência por ID"""
        with self.__db_connection_handler as db:
            dep = db.session.query(EAPItemDependency).options(
                selectinload(EAPItemDependency.successor),
                selectinload(EAPItemDependency.predecessor)
            ).filter(
                EAPItemDependency.id == dependency_id
            ).first()
            
            return self._to_entity(dep) if dep else None
    
    def find_predecessors(self, item_id: int) -> List[EAPDependencyEntity]:
        """Busca todos os predecessores de um item"""
        with self.__db_connection_handler as db:
            deps = db.session.query(EAPItemDependency).options(
                selectinload(EAPItemDependency.successor),
                selectinload(EAPItemDependency.predecessor)
            ).filter(
                EAPItemDependency.successor_id == item_id
            ).all()
            
            return [self._to_entity(dep) for dep in deps]
    
    def find_successors(self, item_id: int) -> List[EAPDependencyEntity]:
        """Busca todos os sucessores de um item"""
        with self.__db_connection_handler as db:
            deps = db.session.query(EAPItemDependency).options(
                selectinload(EAPItemDependency.successor),
                selectinload(EAPItemDependency.predecessor)
            ).filter(
                EAPItemDependency.predecessor_id == item_id
            ).all()
            
            return [self._to_entity(dep) for dep in deps]
    
    def find_all_by_eap(self, eap_id: int) -> List[EAPDependencyEntity]:
        """Busca todas as dependências de uma EAP"""
        with self.__db_connection_handler as db:
            # Busca itens da EAP e suas dependências
            deps = db.session.query(EAPItemDependency).join(
                EAPItem, EAPItem.id == EAPItemDependency.successor_id
            ).filter(
                EAPItem.eap_id == eap_id
            ).options(
                selectinload(EAPItemDependency.successor),
                selectinload(EAPItemDependency.predecessor)
            ).all()
            
            return [self._to_entity(dep) for dep in deps]
    
    def exists(self, successor_id: int, predecessor_id: int) -> bool:
        """Verifica se uma dependência já existe"""
        with self.__db_connection_handler as db:
            count = db.session.query(EAPItemDependency).filter(
                EAPItemDependency.successor_id == successor_id,
                EAPItemDependency.predecessor_id == predecessor_id
            ).count()
            
            return count > 0
    
    def delete(self, dependency_id: int) -> None:
        """Remove uma dependência"""
        with self.__db_connection_handler as db:
            dep = db.session.query(EAPItemDependency).filter(
                EAPItemDependency.id == dependency_id
            ).first()
            
            if dep:
                db.session.delete(dep)
                db.session.commit()
    
    def has_circular_dependency(self, successor_id: int, predecessor_id: int) -> bool:
        """
        Verifica se criar esta dependência geraria um ciclo.
        Usa DFS (busca em profundidade) para detectar ciclos.
        """
        with self.__db_connection_handler as db:
            visited = set()
            
            def dfs(current_id: int) -> bool:
                # Se chegamos no successor original, tem ciclo!
                if current_id == successor_id:
                    return True
                
                # Se já visitamos este nó, não tem ciclo neste caminho
                if current_id in visited:
                    return False
                
                visited.add(current_id)
                
                # Busca todos os predecessores deste nó
                predecessors = db.session.query(EAPItemDependency).filter(
                    EAPItemDependency.successor_id == current_id
                ).all()
                
                # Verifica recursivamente cada predecessor
                for dep in predecessors:
                    if dfs(dep.predecessor_id):
                        return True
                
                return False
            
            # Inicia DFS a partir do predecessor
            return dfs(predecessor_id)
    
    def is_descendant(self, potential_descendant_id: int, ancestor_id: int) -> bool:
        """
        Verifica se um item é descendente (filho/neto/etc) de outro na hierarquia da EAP
        """
        with self.__db_connection_handler as db:
            item = db.session.query(EAPItem).filter(
                EAPItem.id == potential_descendant_id
            ).first()
            
            if not item:
                return False
            
            # Sobe na hierarquia até achar o ancestral ou chegar na raiz
            current = item
            while current.parent_id is not None:
                if current.parent_id == ancestor_id:
                    return True
                current = db.session.query(EAPItem).filter(
                    EAPItem.id == current.parent_id
                ).first()
                if not current:
                    break
            
            return False
    
    def _to_entity(self, model: EAPItemDependency) -> EAPDependencyEntity:
        """Converte model do SQLAlchemy para Entity do domain"""
        if not model:
            return None
        
        return EAPDependencyEntity(
            id=model.id,
            successor_id=model.successor_id,
            predecessor_id=model.predecessor_id,
            dependency_type=DependencyType.from_string(model.dependency_type),
            lag_days=model.lag_days,
            created_at=model.created_at,
            updated_at=model.updated_at,
            # Informações extras se disponíveis
            successor_name=model.successor.name if hasattr(model, 'successor') and model.successor else None,
            successor_code=model.successor.code if hasattr(model, 'successor') and model.successor else None,
            predecessor_name=model.predecessor.name if hasattr(model, 'predecessor') and model.predecessor else None,
            predecessor_code=model.predecessor.code if hasattr(model, 'predecessor') and model.predecessor else None
        )

