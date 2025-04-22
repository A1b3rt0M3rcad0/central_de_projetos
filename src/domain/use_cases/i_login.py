from src.domain.value_objects.password import Password
from src.domain.value_objects.cpf import CPF
from abc import ABC, abstractmethod

class ILogin(ABC):

    @abstractmethod
    def check(self, cpf:CPF, password:Password) -> str:
        """
        Recebe o cpf e password, realiza a busca no banco de dados utilizando cpf,
        coleta o password e salt diretamente do banco de dados, verifica o password, se valido retorna
        um jwt, caso contrario retorna um erro 404 (UserNotFoundError)
        """