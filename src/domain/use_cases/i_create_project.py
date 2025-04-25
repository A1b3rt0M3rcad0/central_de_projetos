from abc import ABC, abstractmethod
from datetime import datetime
from src.domain.value_objects.monetary_value import MonetaryValue
from typing import Optional

class ICreateProject(ABC):

    @abstractmethod
    def create(self, 
               status_id:int,
               name:str, 
               verba_disponivel:Optional[MonetaryValue]=None, 
               andamento_do_projeto:Optional[str]=None, 
               start_date:Optional[datetime]=None, 
               expected_completion_date:Optional[datetime]=None, 
               end_date:Optional[datetime]=None
               ) -> None:
        """
        Cria um novo projeto no banco de dados.

        Apenas o ID do status e o nome do projeto são obrigatórios. Os demais campos são opcionais.

        Parâmetros:
            status_id: ID do status atual do projeto.
            name: Nome do projeto.
            verba_disponivel: (Opcional) Verba disponível para o projeto.
            andamento_do_projeto: (Opcional) Descrição do andamento atual.
            start_date: (Opcional) Data de início do projeto.
            expected_completion_date: (Opcional) Data prevista de conclusão.
            end_date: (Opcional) Data de encerramento do projeto.

        Levanta:
            CreateProjectError (500): Se ocorrer qualquer erro durante a criação do projeto.
        """