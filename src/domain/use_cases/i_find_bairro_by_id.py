from abc import ABC, abstractmethod
from src.domain.entities.bairro import BairroEntity

class IFindBairroById(ABC):

    @abstractmethod
    def find(self, bairro_id:int) -> BairroEntity:
        '''
        Retorna o bairro pelo id

        Parametros:
            bairro_id: id do bairro
        Levanta:
            BairroNotExists; caso n encontrenenhum bairro
        '''