from datetime import datetime
from typing import Optional

from src.domain.entities.eap import EAPEntity, EAPItemEntity
from src.domain.use_cases.i_create_eap import ICreateEAP
from src.domain.use_cases.i_find_eap import IFindEAP
from src.data.interface.i_eap_repository import IEAPRepository
from src.data.interface.i_eap_item_repository import IEAPItemRepository
from src.errors.eap.project_already_has_eap_error import ProjectAlreadyHasEAPError
from src.errors.eap.eap_not_found_error import EAPNotFoundError


class CreateEAP(ICreateEAP):
    """Caso de uso para criação de EAP"""
    
    def __init__(self, eap_repository: IEAPRepository, eap_item_repository: IEAPItemRepository, find_eap_case: IFindEAP):
        self.__eap_repository = eap_repository
        self.__eap_item_repository = eap_item_repository
        self.__find_eap_case = find_eap_case
    
    def create(self, name: str, description: str, project_id: int, created_by: str, template_source_id: Optional[int] = None) -> EAPEntity:
        """
        Cria uma nova EAP
        
        Args:
            name: Nome da EAP
            description: Descrição da EAP
            project_id: ID do projeto ao qual a EAP será vinculada
            created_by: ID do usuário que está criando a EAP
            template_source_id: ID da EAP template que será usada como base (opcional)
        
        Returns:
            EAPEntity: A EAP criada
            
        Raises:
            ValueError: Se os dados fornecidos forem inválidos
            ProjectNotFoundError: Se o projeto não existir
            EAPTemplateNotFoundError: Se a EAP template não existir
            ProjectAlreadyHasEAPError: Se o projeto já possui uma EAP
        """
        # Verifica se o projeto já possui uma EAP
        existing_eap = self.__eap_repository.find_by_project_id(project_id)
        if existing_eap:
            raise ProjectAlreadyHasEAPError(project_id)
        
        # Se foi fornecida uma EAP template, busca ela
        template_items = []
        if template_source_id:
            template_eap = self.__find_eap_case.find_by_id(template_source_id)
            if not template_eap:
                raise EAPNotFoundError(template_source_id)
            
            if not template_eap.is_template:
                raise ValueError("EAP fornecida não é um template")
            
            template_items = template_eap.items
        
        # Cria a nova EAP
        now = datetime.now()
        new_eap = EAPEntity(
            id=None,
            name=name,
            description=description,
            project_id=project_id,
            is_template=False,
            template_source_id=template_source_id,
            created_by=created_by,
            created_at=now,
            updated_at=now,
            items=[]
        )
        
        # Salva a EAP no repositório
        created_eap = self.__eap_repository.create(new_eap)
        
        # Se há itens do template, cria eles na nova EAP
        if template_items:
            self._copy_template_items(created_eap.id, template_items)
            
            # Busca a EAP novamente com os itens
            created_eap = self.__eap_repository.find_by_id(created_eap.id)
        
        return created_eap
    
    def _copy_template_items(self, eap_id: int, template_items: list[EAPItemEntity]) -> None:
        """Copia os itens de um template para uma nova EAP"""
        # Mapeia os IDs antigos para os novos
        id_mapping = {}
        
        # Primeiro, cria todos os itens raiz
        root_items = [item for item in template_items if item.parent_id is None]
        for item in root_items:
            new_item = EAPItemEntity(
                id=None,
                eap_id=eap_id,
                code=item.code,
                name=item.name,
                description=item.description,
                type=item.type,
                parent_id=None,
                responsible=item.responsible,
                start_date=item.start_date,
                end_date=item.end_date,
                budget=item.budget,
                status=item.status,
                progress=0,  # Reseta o progresso
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            created_item = self.__eap_item_repository.create(new_item)
            id_mapping[item.id] = created_item.id
        
        # Depois, cria os itens filhos recursivamente
        self._copy_children_items(eap_id, template_items, id_mapping)
    
    def _copy_children_items(self, eap_id: int, template_items: list[EAPItemEntity], id_mapping: dict) -> None:
        """Copia os itens filhos recursivamente"""
        for template_item in template_items:
            if template_item.parent_id is not None and template_item.parent_id in id_mapping:
                new_parent_id = id_mapping[template_item.parent_id]
                
                new_item = EAPItemEntity(
                    id=None,
                    eap_id=eap_id,
                    code=template_item.code,
                    name=template_item.name,
                    description=template_item.description,
                    type=template_item.type,
                    parent_id=new_parent_id,
                    responsible=template_item.responsible,
                    start_date=template_item.start_date,
                    end_date=template_item.end_date,
                    budget=template_item.budget,
                    status=template_item.status,
                    progress=0,  # Reseta o progresso
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                
                created_item = self.__eap_item_repository.create(new_item)
                id_mapping[template_item.id] = created_item.id
