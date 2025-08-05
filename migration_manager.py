#pylint:disable=all
#pylint:disable=too-many-functions-arg
#!/usr/bin/env python3
"""
Script de Gerenciamento de Migrações
Permite executar migrações Alembic em bancos de teste e produção usando variáveis de ambiente.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env se existir
load_dotenv()

class MigrationManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.alembic_ini = self.project_root / "alembic.ini"
        
    def get_database_url(self, environment: str) -> str:
        """Obtém a URL do banco de dados baseada no ambiente."""
        if environment == "test":
            # Banco de teste
            host = os.getenv("THOST", "localhost")
            port = os.getenv("TPORT", "3306")
            user = os.getenv("TUSERNAME", "root")
            password = os.getenv("TPASSWORD", "")
            database = os.getenv("TDATABASE_NAME", "test_central_de_projetos")
        else:
            # Banco de produção
            host = os.getenv("HOST", "localhost")
            port = os.getenv("PORT", "3306")
            user = os.getenv("USERNAME", "root")
            password = os.getenv("PASSWORD", "")
            database = os.getenv("DATABASE_NAME", "central_de_projetos")
        
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    
    def run_alembic_command(self, command: str, environment: str) -> bool:
        """Executa um comando Alembic com a URL do banco configurada."""
        try:
            # Configura a URL do banco temporariamente
            db_url = self.get_database_url(environment)
            
            # Executa o comando Alembic
            cmd = [
                sys.executable, "-m", "alembic",
                *command.split()
            ]
            
            # Configura as variáveis de ambiente
            env = os.environ.copy()
            env["ALEMBIC_DATABASE_URL"] = db_url
            
            print(f"\n🔄 Executando: {' '.join(cmd)}")
            print(f"📊 Ambiente: {environment.upper()}")
            print(f"🗄️  Banco: {db_url.split('@')[1] if '@' in db_url else 'N/A'}")
            print("-" * 60)
            
            result = subprocess.run(
                cmd,
                env=env,
                cwd=self.project_root,
                capture_output=False,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                print(f"✅ Comando executado com sucesso no ambiente {environment.upper()}")
                return True
            else:
                print(f"❌ Erro ao executar comando no ambiente {environment.upper()}")
                return False
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False
    
    def confirm_action(self, action: str, environments: list) -> bool:
        """Solicita confirmação do usuário."""
        print(f"\n🤔 Você está prestes a executar: {action}")
        print(f"🎯 Ambientes: {', '.join(environments).upper()}")
        
        while True:
            response = input("\n❓ Continuar? (s/n): ").lower().strip()
            if response in ['s', 'sim', 'y', 'yes']:
                return True
            elif response in ['n', 'não', 'no']:
                return False
            else:
                print("❌ Resposta inválida. Digite 's' para sim ou 'n' para não.")
    
    def run_migration(self, action: str, revision: Optional[str] = None, environments: Optional[list] = None):
        """Executa uma migração nos ambientes especificados."""
        if environments is None:
            environments = []
        
        if not environments:
            print("❌ Nenhum ambiente especificado!")
            return
        
        # Confirma a ação
        if not self.confirm_action(action, environments):
            print("❌ Operação cancelada pelo usuário.")
            return
        
        # Executa em cada ambiente
        success_count = 0
        for env in environments:
            if self.run_alembic_command(action, env):
                success_count += 1
        
        # Resumo
        print(f"\n📊 Resumo:")
        print(f"✅ Sucessos: {success_count}/{len(environments)}")
        print(f"❌ Falhas: {len(environments) - success_count}/{len(environments)}")
        
        if success_count == len(environments):
            print("🎉 Todas as operações foram concluídas com sucesso!")
        else:
            print("⚠️  Algumas operações falharam. Verifique os logs acima.")

def main():
    parser = argparse.ArgumentParser(
        description="Gerenciador de Migrações Alembic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python migration_manager.py upgrade head --test --prod
  python migration_manager.py downgrade 81f36764d1ba --test
  python migration_manager.py current --prod
  python migration_manager.py history --test --prod
        """
    )
    
    # Comando Alembic
    parser.add_argument(
        "command",
        help="Comando Alembic (ex: upgrade head, downgrade, current, history)"
    )
    
    # Revisão (opcional)
    parser.add_argument(
        "revision",
        nargs="?",
        help="Revisão específica (ex: 81f36764d1ba)"
    )
    
    # Ambientes
    parser.add_argument(
        "--test",
        action="store_true",
        help="Executar no banco de teste"
    )
    
    parser.add_argument(
        "--prod",
        action="store_true",
        help="Executar no banco de produção"
    )
    
    # Opção para ambos os ambientes
    parser.add_argument(
        "--all",
        action="store_true",
        help="Executar em ambos os ambientes (teste e produção)"
    )
    
    args = parser.parse_args()
    
    # Determina os ambientes
    environments = []
    if args.all or (not args.test and not args.prod):
        environments = ["test", "prod"]
    else:
        if args.test:
            environments.append("test")
        if args.prod:
            environments.append("prod")
    
    # Cria o comando completo
    command = args.command
    if args.revision:
        command += f" {args.revision}"
    
    manager = MigrationManager()
    manager.run_migration(command, args.revision, environments)

if __name__ == "__main__":
    main() 