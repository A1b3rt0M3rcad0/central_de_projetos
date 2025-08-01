from typing import List
from sqlalchemy import String, DateTime, ForeignKey, Float, Integer
from datetime import datetime
from src.infra.relational.config.base.base_model import BaseModel
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Project(BaseModel):

    __tablename__ = 'project'

    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status_id:Mapped[int] = mapped_column(Integer, ForeignKey('status.id'), nullable=False)
    name:Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    verba_disponivel:Mapped[float] = mapped_column(Float, nullable=True)
    andamento_do_projeto:Mapped[str] = mapped_column(String(255), nullable=True)
    start_date:Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expected_completion_date:Mapped[datetime] = mapped_column(DateTime, nullable=True)
    end_date:Mapped[datetime] = mapped_column(DateTime, nullable=True)

    history_projects:Mapped[List["HistoryProject"]] = relationship("HistoryProject", back_populates="project", lazy="selectin")
    project_fiscals:Mapped[List["ProjectFiscal"]] = relationship("ProjectFiscal", back_populates="project", lazy="selectin")
    project_bairros:Mapped[List["ProjectBairro"]] = relationship("ProjectBairro", back_populates="project", lazy="selectin")
    project_empresas:Mapped[List["ProjectEmpresa"]] = relationship("ProjectEmpresa", back_populates="project", lazy="selectin")
    project_types:Mapped[List["ProjectType"]] = relationship("ProjectType", back_populates="project", lazy="selectin")
    user_projects:Mapped[List["UserProject"]] = relationship("UserProject", back_populates="project", lazy="selectin")
    status:Mapped["Status"] = relationship("Status", back_populates="projects", lazy="joined")
    work_projects:Mapped[List["WorkProject"]] = relationship("WorkProject", back_populates="project", lazy="selectin")