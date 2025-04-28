from src.domain.value_objects.cpf import CPF

class RefreshTokenEntity:

    def __init__(self, cpf:CPF, token:str) -> None:
        self.cpf = cpf
        self.token= token