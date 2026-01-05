#pylint:disable=all
# Importar BaseModel primeiro
from src.infra.relational.config.base.base_model import BaseModel

# Importar models base (sem dependências de relacionamento)
from .bairro import Bairro
from .empresa import Empresa
from .fiscal import Fiscal
from .folder import Folder
from .status import Status
from .types import Types
from .user import User

# Importar models de relacionamento (dependem dos models base)
# IMPORTANTE: ProjectFolder deve ser importado ANTES do Project
from .history_project import HistoryProject
from .project_bairro import ProjectBairro
from .project_empresa import ProjectEmpresa
from .project_fiscal import ProjectFiscal
from .project_folder import ProjectFolder  # Importar ANTES do Project
from .project_type import ProjectType
from .user_project import UserProject
from .refresh_token import RefreshToken
from .work_project import WorkProject

# Importar Project DEPOIS de todos os relacionamentos
from .project import Project

# Importar models complexos (EAP tem relacionamentos próprios)
from .eap import EAP, EAPItem
