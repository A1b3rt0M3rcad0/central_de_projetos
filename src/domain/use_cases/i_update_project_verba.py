from src.domain.value_objects.monetary_value import MonetaryValue
from abc import ABC, abstractmethod

class IUpdateProjectVerba(ABC):

    @abstractmethod
    def update(self, project_id:int, verba_disponivel:MonetaryValue) -> None:
        '''
        Coleta o project_id e a nova verba para alterar no banco de dados a antiga verba,
        caso n consiga alterar a antiga verba no banco de dados, retorne 500 InternalServerError
        '''