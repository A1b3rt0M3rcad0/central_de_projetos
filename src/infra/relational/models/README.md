SQLAlchemy v2.0 - GPP (Gestor de Processos Públicos)

Este projeto utiliza a versão 2.0 do SQLAlchemy para mapeamento objeto-relacional (ORM), oferecendo uma forma moderna e robusta de interagir com o banco de dados. A versão 2.0 traz melhorias significativas em performance e, principalmente, uma sintaxe mais limpa e orientada a tipos, alinhando o uso do ORM com as práticas mais recentes do Python.

Estrutura dos Modelos

Os modelos de dados são definidos usando o estilo "Declarative with Mapped Annotations" e mapped_column, que é o padrão recomendado para o SQLAlchemy 2.0. Isso garante uma integração mais fluida com type hints do Python, facilitando a detecção de erros e melhorando a legibilidade do código.

Base Declarativa

A base para todos os modelos é BaseModel, definida em src/infra/relational/config/base/base_model.py. Esta classe herda de DeclarativeBase (ou similar, dependendo da sua configuração), fornecendo a infraestrutura necessária para o mapeamento ORM.

Modelos Principais

A seguir, uma visão geral dos modelos de entidade e de relacionamento definidos no projeto:

    User: Representa os usuários do sistema, contendo informações como CPF, nome, senha (hashed), salt, papel (role) e email.

        Relacionamentos:

            user_projects: Mapeia para as associações UserProject, indicando os projetos aos quais o usuário está atribuído (relação um-para-muitos).

            refresh_token: Mapeia para o token de refresh do usuário (relação um-para-um).

    Project: Gerencia as informações dos projetos, incluindo status, verba, andamento, datas e metadados como nome.

        Relacionamentos:

            history_projects: Rastreia o histórico de alterações do projeto.

            project_fiscals: Associa fiscais ao projeto.

            project_bairros: Associa bairros ao projeto.

            project_empresas: Associa empresas ao projeto.

            project_types: Associa tipos de projeto ao projeto.

            status: Relacionamento com o status atual do projeto (relação muitos-para-um).

            user_projects: NOVO! Mapeia para as associações UserProject, indicando os usuários atribuídos a este projeto (relação um-para-muitos).

    Status: Define os possíveis status que um projeto pode ter (ex: Ativo, Concluído, Em Andamento).

        Relacionamentos:

            projects: Mapeia para os projetos que possuem este status.

    Fiscal: Representa os fiscais associados a projetos.

        Relacionamentos:

            project_fiscals: Mapeia para as associações ProjectFiscal.

    Bairro: Define os bairros que podem ser associados a projetos.

        Relacionamentos:

            project_bairros: Mapeia para as associações ProjectBairro.

    Empresa: Representa as empresas envolvidas nos projetos.

        Relacionamentos:

            project_empresas: Mapeia para as associações ProjectEmpresa.

    Types: Define os tipos de projetos.

        Relacionamentos:

            project_types: Mapeia para as associações ProjectType.

Modelos de Associação (Tabelas de Junção)

Para gerenciar relacionamentos muitos-para-muitos, ou adicionar atributos extras a um relacionamento, são utilizadas tabelas de associação explícitas:

    UserProject: Tabela de associação entre User e Project. Contém user_cpf, project_id e assignment_date.

        Relacionamentos: user (para o User associado) e project (para o Project associado).

    ProjectBairro: Tabela de associação entre Project e Bairro.

        Relacionamentos: project e bairro.

    ProjectEmpresa: Tabela de associação entre Project e Empresa.

        Relacionamentos: project e empresa.

    ProjectFiscal: Tabela de associação entre Project e Fiscal.

        Relacionamentos: project e fiscal.

    ProjectType: Tabela de associação entre Project e Types.

        Relacionamentos: project e types.

    RefreshToken: Tabela para armazenar tokens de refresh, associada ao User.

        Relacionamentos: user.

    HistoryProject: Registra alterações em projetos.

        Relacionamentos: project.

Configuração de Relacionamentos

Todos os relacionamentos são definidos com relationship() e utilizam back_populates para criar links bidirecionais entre os modelos, garantindo que você possa navegar facilmente entre objetos relacionados em ambas as direções. O carregamento "lazy loading" é configurado predominantemente com lazy="selectin", que otimiza o carregamento de coleções ao executar uma única consulta JOIN para buscar os dados relacionados de forma eficiente. Para relacionamentos um-para-um ou muitos-para-um, lazy="joined" pode ser usado para carregar o objeto relacionado imediatamente com a consulta principal.

Como Usar (Exemplo Básico)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.relational.config.base.base_model import BaseModel # Sua base declarativa
from src.infra.relational.model.project import Project
from src.infra.relational.model.user import User
from src.infra.relational.model.user_project import UserProject
from datetime import datetime, timezone

# 1. Configurar o Engine (adapte sua string de conexão)

DATABASE_URL = "sqlite:///./your_database.db" # Exemplo para SQLite
engine = create_engine(DATABASE_URL)

# 2. Criar as tabelas no banco de dados (se não existirem)

BaseModel.metadata.create_all(engine)

# 3. Criar uma sessão

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with Session() as session: # Exemplo: Adicionar um novo usuário
new_user = User(
cpf="123.456.789-00",
name="João Silva",
password=b"hashed_password", # Em um cenário real, você usaria sua lógica de hash
salt=b"random_salt",
role="Desenvolvedor",
email="joao.silva@example.com",
created_at=datetime.now(timezone.utc)
)
session.add(new_user)
session.commit()
session.refresh(new_user)
print(f"Usuário criado: {new_user.name} (CPF: {new_user.cpf})")

    # Exemplo: Adicionar um novo projeto
    new_project = Project(
        status_id=1, # Supondo que você tenha um Status com ID 1
        name="Projeto Alpha",
        verba_disponivel=10000.00,
        andamento_do_projeto="Em Andamento",
        start_date=datetime.now(timezone.utc),
        expected_completion_date=datetime(2026, 12, 31, tzinfo=timezone.utc),
        created_at=datetime.now(timezone.utc)
    )
    session.add(new_project)
    session.commit()
    session.refresh(new_project)
    print(f"Projeto criado: {new_project.name} (ID: {new_project.id})")

    # Exemplo: Atribuir o usuário ao projeto
    new_user_project = UserProject(
        user=new_user, # Atribua o objeto User
        project=new_project, # Atribua o objeto Project
        assignment_date=datetime.now(timezone.utc)
    )
    session.add(new_user_project)
    session.commit()
    session.refresh(new_user_project)
    print(f"Usuário {new_user.name} atribuído ao projeto {new_project.name}")

    # Exemplo: Buscar um projeto e seus usuários atribuídos
    project_with_users = session.query(Project).filter_by(id=new_project.id).first()
    if project_with_users:
        print(f"\nDetalhes do Projeto: {project_with_users.name}")
        for up in project_with_users.user_projects:
            print(f"  - Usuário Atribuído: {up.user.name} (CPF: {up.user.cpf}), Atribuído em: {up.assignment_date}")

    session.close()
