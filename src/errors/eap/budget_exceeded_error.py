from src.errors.eap.base_eap_error import BaseEAPError


class BudgetExceededError(BaseEAPError):
    """Erro quando o orçamento dos filhos excede o orçamento do pai"""
    
    def __init__(self, parent_name: str, parent_budget: float, children_budget: float):
        self.parent_name = parent_name
        self.parent_budget = parent_budget
        self.children_budget = children_budget
        self.exceeded_amount = children_budget - parent_budget
        
        super().__init__(
            status_code=400,
            message=f"Orçamento excedido no item '{parent_name}'. "
                   f"Orçamento disponível: R$ {parent_budget:,.2f}, "
                   f"Orçamento dos filhos: R$ {children_budget:,.2f}, "
                   f"Excesso: R$ {self.exceeded_amount:,.2f}"
        )
