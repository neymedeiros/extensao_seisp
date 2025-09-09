import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class DatabaseConnection:
    """
    Classe para gerenciar a conexão com o banco PostgreSQL
    """
    
    def __init__(self):
        """
        Inicializa a conexão com o banco usando as variáveis de ambiente
        """
        self.host = os.getenv('DB_HOST')
        self.port = os.getenv('DB_PORT')
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.schema = os.getenv('DB_SCHEMA', 'public')  # Schema padrão é 'public'
        self.connection = None
    
    def conectar(self):
        """
        Estabelece conexão com o banco de dados
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor,  # Retorna resultados como dicionário
                options=f"-c search_path={self.schema}"  # Define o schema
            )
            print("✅ Conexão estabelecida com sucesso!")
            return True
        except psycopg2.Error as erro:
            print(f"❌ Erro ao conectar com o banco: {erro}")
            return False
    
    def desconectar(self):
        """
        Fecha a conexão com o banco de dados
        """
        if self.connection:
            self.connection.close()
            print("🔌 Conexão fechada.")
    
    def testar_conexao(self):
        """
        Testa se a conexão está funcionando
        """
        if not self.connection:
            print("❌ Não há conexão ativa.")
            return False
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT version();")
            versao = cursor.fetchone()
            print(f"🐘 PostgreSQL versão: {versao['version']}")
            cursor.close()
            return True
        except psycopg2.Error as erro:
            print(f"❌ Erro ao testar conexão: {erro}")
            return False

# Exemplo de uso
if __name__ == "__main__":
    # Cria uma instância da conexão
    db = DatabaseConnection()
    
    # Tenta conectar
    if db.conectar():
        # Testa a conexão
        db.testar_conexao()
        
        # Fecha a conexão
        db.desconectar()
    else:
        print("Não foi possível estabelecer conexão com o banco.")