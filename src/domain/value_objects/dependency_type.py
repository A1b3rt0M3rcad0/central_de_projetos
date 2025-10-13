"""
Value Object para tipo de dependência entre itens da EAP
"""
from enum import Enum


class DependencyType(Enum):
    """
    Enum que representa os tipos de dependências entre itens da EAP.
    
    Baseado no padrão PMI (Project Management Institute):
    - FS (Finish-to-Start): Mais comum (~90% dos casos)
    - SS (Start-to-Start): Tarefas que começam juntas
    - FF (Finish-to-Finish): Tarefas que terminam juntas
    - SF (Start-to-Finish): Raro, usado em casos específicos
    """
    
    FINISH_TO_START = "FS"
    START_TO_START = "SS"
    FINISH_TO_FINISH = "FF"
    START_TO_FINISH = "SF"
    
    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        return self.value
    
    def get_display_name(self) -> str:
        """Retorna o nome de exibição do tipo"""
        display_names = {
            self.FINISH_TO_START: "Término → Início",
            self.START_TO_START: "Início → Início",
            self.FINISH_TO_FINISH: "Término → Término",
            self.START_TO_FINISH: "Início → Término"
        }
        return display_names[self]
    
    def get_description(self) -> str:
        """Retorna a descrição detalhada do tipo"""
        descriptions = {
            self.FINISH_TO_START: "O predecessor deve terminar antes do sucessor começar (mais comum)",
            self.START_TO_START: "O sucessor só pode começar quando o predecessor começar",
            self.FINISH_TO_FINISH: "O sucessor só pode terminar quando o predecessor terminar",
            self.START_TO_FINISH: "O sucessor só pode terminar quando o predecessor começar (raro)"
        }
        return descriptions[self]
    
    def get_icon(self) -> str:
        """Retorna o ícone associado ao tipo"""
        icons = {
            self.FINISH_TO_START: "→",
            self.START_TO_START: "⇉",
            self.FINISH_TO_FINISH: "⇄",
            self.START_TO_FINISH: "⇇"
        }
        return icons[self]
    
    @classmethod
    def from_string(cls, value: str) -> 'DependencyType':
        """Cria DependencyType a partir de string"""
        for dep_type in cls:
            if dep_type.value == value.upper():
                return dep_type
        raise ValueError(f"Tipo de dependência inválido: {value}")

