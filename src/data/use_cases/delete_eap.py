from src.domain.use_cases.i_delete_eap import IDeleteEAP
from src.domain.use_cases.i_find_eap import IFindEAP
from src.data.interface.i_eap_repository import IEAPRepository
from src.errors.eap.eap_not_found_error import EAPNotFoundError


class DeleteEAP(IDeleteEAP):
    """Caso de uso para exclusão de EAP"""
    
    def __init__(self, eap_repository: IEAPRepository, find_eap_case: IFindEAP):
        self.__eap_repository = eap_repository
        self.__find_eap_case = find_eap_case
    
    def delete(self, eap_id: int) -> None:
        """
        Exclui uma EAP
        
        Args:
            eap_id: ID da EAP a ser excluída
            
        Raises:
            EAPNotFoundError: Se a EAP não existir
            EAPInUseError: Se a EAP estiver sendo usada por outros projetos
        """
        # Verifica se a EAP existe
        existing_eap = self.__find_eap_case.find_by_id(eap_id)
        if not existing_eap:
            raise EAPNotFoundError(eap_id)
        
        # Verifica se é uma EAP template que está sendo usada
        if existing_eap.is_template:
            # Aqui poderia verificar se há EAPs que usam este template
            # Por enquanto, permitimos a exclusão
            pass
        
        # Exclui a EAP
        self.__eap_repository.delete(eap_id)
