from src.errors.eap.base_eap_error import BaseEAPError


class ProjectAlreadyHasEAPError(BaseEAPError):
    """Erro quando um projeto já possui uma EAP"""
    
    def __init__(self, project_id: int):
        self.project_id = project_id
        super().__init__(
            status_code=409,
            message=f"Projeto com ID {project_id} já possui uma EAP"
        )
