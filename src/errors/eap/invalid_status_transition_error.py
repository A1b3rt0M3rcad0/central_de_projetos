from src.errors.eap.base_eap_error import BaseEAPError


class InvalidStatusTransitionError(BaseEAPError):
    """Erro quando uma transição de status é inválida"""
    
    def __init__(self, current_status: str, target_status: str):
        self.current_status = current_status
        self.target_status = target_status
        super().__init__(
            status_code=400,
            message=f"Transição de status inválida: de {current_status} para {target_status}"
        )
