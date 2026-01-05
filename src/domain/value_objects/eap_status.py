from enum import Enum


class EAPStatus(Enum):  # pylint: disable=too-many-public-methods
    """Enum que representa os status possíveis de um item da EAP"""
    
    NAO_INICIADO = "nao_iniciado"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"
    PAUSADO = "pausado"
    CANCELADO = "cancelado"
    BLOQUEADO = "bloqueado"
    
    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        return self.value
    
    def get_display_name(self) -> str:
        """Retorna o nome de exibição do status"""
        display_names = {
            self.NAO_INICIADO: "Não Iniciado",
            self.EM_ANDAMENTO: "Em Andamento",
            self.CONCLUIDO: "Concluído",
            self.PAUSADO: "Pausado",
            self.CANCELADO: "Cancelado",
            self.BLOQUEADO: "Bloqueado"
        }
        return display_names[self]
    
    def get_description(self) -> str:
        """Retorna a descrição do status"""
        descriptions = {
            self.NAO_INICIADO: "Item ainda não foi iniciado",
            self.EM_ANDAMENTO: "Item está sendo executado",
            self.CONCLUIDO: "Item foi finalizado com sucesso",
            self.PAUSADO: "Item foi temporariamente pausado",
            self.CANCELADO: "Item foi cancelado",
            self.BLOQUEADO: "Item está bloqueado por dependência"
        }
        return descriptions[self]
    
    def get_color(self) -> str:
        """Retorna a cor associada ao status"""
        colors = {
            self.NAO_INICIADO: "gray",
            self.EM_ANDAMENTO: "blue",
            self.CONCLUIDO: "green",
            self.PAUSADO: "yellow",
            self.CANCELADO: "red",
            self.BLOQUEADO: "orange"
        }
        return colors[self]
    
    def get_icon(self) -> str:
        """Retorna o ícone associado ao status"""
        icons = {
            self.NAO_INICIADO: "⏳",
            self.EM_ANDAMENTO: "🔄",
            self.CONCLUIDO: "✅",
            self.PAUSADO: "⏸️",
            self.CANCELADO: "❌",
            self.BLOQUEADO: "🚫"
        }
        return icons[self]
    
    def is_active(self) -> bool:
        """Verifica se o status indica que o item está ativo"""
        return self in [self.EM_ANDAMENTO, self.PAUSADO, self.BLOQUEADO]
    
    def is_finished(self) -> bool:
        """Verifica se o status indica que o item foi finalizado"""
        return self in [self.CONCLUIDO, self.CANCELADO]
    
    def is_blocked(self) -> bool:
        """Verifica se o status indica que o item está bloqueado"""
        return self == self.BLOQUEADO
    
    def can_start(self) -> bool:
        """Verifica se o item pode ser iniciado a partir deste status"""
        return self == self.NAO_INICIADO
    
    def can_pause(self) -> bool:
        """Verifica se o item pode ser pausado a partir deste status"""
        return self == self.EM_ANDAMENTO
    
    def can_resume(self) -> bool:
        """Verifica se o item pode ser retomado a partir deste status"""
        return self == self.PAUSADO
    
    def can_complete(self) -> bool:
        """Verifica se o item pode ser concluído a partir deste status"""
        return self in [self.EM_ANDAMENTO, self.PAUSADO]
    
    def can_cancel(self) -> bool:
        """Verifica se o item pode ser cancelado a partir deste status"""
        return self not in [self.CONCLUIDO, self.CANCELADO]
    
    def can_block(self) -> bool:
        """Verifica se o item pode ser bloqueado a partir deste status"""
        return self in [self.NAO_INICIADO, self.EM_ANDAMENTO]
    
    def can_unblock(self) -> bool:
        """Verifica se o item pode ser desbloqueado a partir deste status"""
        return self == self.BLOQUEADO
    
    def get_allowed_transitions(self) -> list['EAPStatus']:
        """Retorna os status para os quais este status pode transicionar"""
        transitions = {
            self.NAO_INICIADO: [self.EM_ANDAMENTO, self.BLOQUEADO, self.CANCELADO],
            self.EM_ANDAMENTO: [self.CONCLUIDO, self.PAUSADO, self.BLOQUEADO, self.CANCELADO],
            self.PAUSADO: [self.EM_ANDAMENTO, self.CANCELADO],
            self.BLOQUEADO: [self.NAO_INICIADO, self.EM_ANDAMENTO],
            self.CONCLUIDO: [],
            self.CANCELADO: []
        }
        return transitions[self]
    
    def can_transition_to(self, target_status: 'EAPStatus') -> bool:
        """Verifica se é possível transicionar para um status específico"""
        return target_status in self.get_allowed_transitions()
    
    @classmethod
    def from_string(cls, value: str) -> 'EAPStatus':
        """Cria um EAPStatus a partir de uma string"""
        try:
            return cls(value.lower())
        except ValueError as exc:
            raise ValueError(f"Status EAP inválido: {value}") from exc
    
    @classmethod
    def get_active_statuses(cls) -> list['EAPStatus']:
        """Retorna todos os status ativos"""
        return [status for status in cls if status.is_active()]
    
    @classmethod
    def get_finished_statuses(cls) -> list['EAPStatus']:
        """Retorna todos os status finalizados"""
        return [status for status in cls if status.is_finished()]
    
    @classmethod
    def get_all_statuses(cls) -> list['EAPStatus']:
        """Retorna todos os status disponíveis"""
        return list(cls)
