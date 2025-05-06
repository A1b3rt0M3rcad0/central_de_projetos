from sqlalchemy import String, Column, DateTime, Integer, ForeignKey, Float
from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy.orm import backref, relationship
from src.infra.relational.models.history_project import HistoryProject
from src.infra.relational.models.project_fiscal import ProjectFiscal
from src.infra.relational.models.project_bairro import ProjectBairro
from src.infra.relational.models.project_empresa import ProjectEmpresa
from src.infra.relational.models.project_type import ProjectType

class Project(BaseModel):

    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    status_id = Column(ForeignKey('status.id'), nullable=False)
    name = Column(String(255), unique=True, nullable=True)
    verba_disponivel = Column(Float, nullable=True)
    andamento_do_projeto = Column(String(255), nullable=True)
    start_date = Column(DateTime, nullable=True)
    expected_completion_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    history_project = relationship(HistoryProject, backref=backref('project'))
    project_fiscal = relationship(ProjectFiscal, backref=backref('project'))
    project_bairro = relationship(ProjectBairro, backref=backref('project'))
    project_empresa = relationship(ProjectEmpresa, backref=backref('project'))
    project_types = relationship(ProjectType, backref=backref('project'))