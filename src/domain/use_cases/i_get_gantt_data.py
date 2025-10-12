"""Interface Get Gantt Data"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class IGetGanttData(ABC):  # pylint: disable=too-few-public-methods
    """Interface para buscar dados formatados para Gantt Chart"""

    @abstractmethod
    def execute(self, project_id: int) -> Dict[str, Any]:
        """
        Busca todos os dados necessários para o Gantt Chart

        Args:
            project_id: ID do projeto

        Returns:
            Dict contendo:
                - project: Dados básicos do projeto
                - eap: Dados da EAP formatados
                - tasks: Lista de tarefas no formato Gantt
                - links: Lista de dependências (futuro)
                - statistics: Estatísticas calculadas
        """
