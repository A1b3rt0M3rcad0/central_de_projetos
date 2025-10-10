from src.errors.eap.base_eap_error import BaseEAPError


class DuplicateEAPCodeError(BaseEAPError):
    """Erro quando o código da EAP já existe"""
    
    def __init__(self, code: str, eap_id: int):
        self.code = code
        self.eap_id = eap_id
        super().__init__(
            status_code=409,
            message=f"Código EAP {code} já existe na EAP {eap_id}"
        )
