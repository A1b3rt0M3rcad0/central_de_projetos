from enum import Enum


class EAPType(Enum):
    """Enum que representa os tipos de itens da EAP"""
    
    FASE = "fase"
    ENTREGA = "entrega"
    ATIVIDADE = "atividade"
    TAREFA = "tarefa"
    
    def __str__(self) -> str:
        return self.value
    
    def get_display_name(self) -> str:
        """Retorna o nome de exibição do tipo"""
        display_names = {
            self.FASE: "Fase",
            self.ENTREGA: "Entrega",
            self.ATIVIDADE: "Atividade",
            self.TAREFA: "Tarefa"
        }
        return display_names[self]
    
    def get_description(self) -> str:
        """Retorna a descrição do tipo"""
        descriptions = {
            self.FASE: "Agrupamento principal de trabalho",
            self.ENTREGA: "Resultado tangível esperado",
            self.ATIVIDADE: "Trabalho executável específico",
            self.TAREFA: "Unidade mínima de trabalho"
        }
        return descriptions[self]
    
    def get_icon(self) -> str:
        """Retorna o ícone associado ao tipo"""
        icons = {
            self.FASE: "📋",
            self.ENTREGA: "📦",
            self.ATIVIDADE: "✅",
            self.TAREFA: "🔧"
        }
        return icons[self]
    
    def get_color(self) -> str:
        """Retorna a cor associada ao tipo"""
        colors = {
            self.FASE: "blue",
            self.ENTREGA: "green",
            self.ATIVIDADE: "purple",
            self.TAREFA: "orange"
        }
        return colors[self]
    
    def can_have_children(self) -> bool:
        """Verifica se este tipo pode ter itens filhos"""
        return self in [self.FASE, self.ENTREGA, self.ATIVIDADE]
    
    def get_allowed_child_types(self) -> list['EAPType']:
        """Retorna os tipos permitidos como filhos"""
        allowed_children = {
            self.FASE: [self.ENTREGA, self.ATIVIDADE],
            self.ENTREGA: [self.ATIVIDADE, self.TAREFA],
            self.ATIVIDADE: [self.TAREFA],
            self.TAREFA: []
        }
        return allowed_children[self]
    
    def is_valid_child_type(self, child_type: 'EAPType') -> bool:
        """Verifica se um tipo pode ser filho deste tipo"""
        return child_type in self.get_allowed_child_types()
    
    @classmethod
    def get_root_types(cls) -> list['EAPType']:
        """Retorna os tipos que podem ser itens raiz"""
        return [cls.FASE]
    
    @classmethod
    def from_string(cls, value: str) -> 'EAPType':
        """Cria um EAPType a partir de uma string"""
        try:
            return cls(value.lower())
        except ValueError as exc:
            raise ValueError(f"Tipo EAP inválido: {value}") from exc
    
    @classmethod
    def get_all_types(cls) -> list['EAPType']:
        """Retorna todos os tipos disponíveis"""
        return list(cls)
