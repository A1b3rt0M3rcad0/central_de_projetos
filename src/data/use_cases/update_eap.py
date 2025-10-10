from datetime import datetime
from typing import Optional

from src.domain.entities.eap import EAPEntity
from src.domain.use_cases.i_update_eap import IUpdateEAP
from src.domain.use_cases.i_find_eap import IFindEAP
from src.data.interface.i_eap_repository import IEAPRepository
from src.errors.eap.eap_not_found_error import EAPNotFoundError


class UpdateEAP(IUpdateEAP):
    """Caso de uso para atualização de EAP"""
    
    def __init__(self, eap_repository: IEAPRepository, find_eap_case: IFindEAP):
        self.__eap_repository = eap_repository
        self.__find_eap_case = find_eap_case
    
    def update(self, eap_id: int, name: Optional[str] = None, description: Optional[str] = None) -> EAPEntity:
        """
        Atualiza os dados básicos de uma EAP
        
        Args:
            eap_id: ID da EAP
            name: Novo nome da EAP (opcional)
            description: Nova descrição da EAP (opcional)
            
        Returns:
            EAPEntity: A EAP atualizada
            
        Raises:
            EAPNotFoundError: Se a EAP não existir
            ValueError: Se os dados fornecidos forem inválidos
        """
        # Busca a EAP existente
        existing_eap = self.__find_eap_case.find_by_id(eap_id)
        if not existing_eap:
            raise EAPNotFoundError(eap_id)
        
        # Valida os novos dados
        if name is not None and not name.strip():
            raise ValueError("Nome da EAP não pode estar vazio")
        
        if description is not None and not description.strip():
            raise ValueError("Descrição da EAP não pode estar vazia")
        
        # Cria uma nova instância com os dados atualizados
        updated_eap = EAPEntity(
            id=existing_eap.id,
            name=name if name is not None else existing_eap.name,
            description=description if description is not None else existing_eap.description,
            project_id=existing_eap.project_id,
            is_template=existing_eap.is_template,
            template_source_id=existing_eap.template_source_id,
            created_by=existing_eap.created_by,
            created_at=existing_eap.created_at,
            updated_at=datetime.now(),
            items=existing_eap.items
        )
        
        # Salva as alterações
        return self.__eap_repository.update(updated_eap)
