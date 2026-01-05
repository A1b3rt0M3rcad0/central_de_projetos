from src.errors.eap.base_eap_error import BaseEAPError


class EAPNotFoundError(BaseEAPError):
    """Erro quando uma EAP não é encontrada"""
    
    def __init__(self, eap_id: int):
        self.eap_id = eap_id
        super().__init__(
            status_code=404,
            message=f"EAP com ID {eap_id} não encontrada"
        )
