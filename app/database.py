import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from contextlib import contextmanager

# Carrega as variáveis do arquivo .env
load_dotenv()

class DatabaseManager:
    """
    Gerenciador de conexão com PostgreSQL para FastAPI
    """
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', '10.0.1.42')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'Banco_X')
        self.user = os.getenv('DB_USER', 'usuario_X')
        self.password = os.getenv('DB_PASSWORD', 'senha_x')
        self.schema = os.getenv('DB_SCHEMA', 'operacoes_inteligencia')
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para conexões - fecha automaticamente
        """
        connection = None
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor,
                options=f"-c search_path={self.schema}"
            )
            yield connection
        except psycopg2.Error as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()
    
    def test_connection(self):
        """
        Testa a conexão com o banco
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                cursor.close()
                return True, version['version']
        except Exception as e:
            return False, str(e)
    
    def consultar_nfe_por_cpf(self, cpf: str):
        """
        Consulta exata por CPF (sem LIKE para performance)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT cpf_dest, nome_dest, fone, data_compra 
                    FROM dim_nfe 
                    WHERE cpf_dest = %s
                    ORDER BY data_compra DESC, nome_dest
                    LIMIT 100
                """
                
                cursor.execute(query, (cpf,))
                resultados = cursor.fetchall()
                cursor.close()
                
                return True, resultados
                
        except Exception as e:
            return False, str(e)
    
    def consultar_nfe_por_nome(self, nome: str):
        """
        Consulta exata por nome (sem LIKE para performance)
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT cpf_dest, nome_dest, fone, data_compra 
                    FROM dim_nfe 
                    WHERE nome_dest = %s
                    ORDER BY data_compra DESC, nome_dest
                    LIMIT 100
                """
                
                cursor.execute(query, (nome,))
                resultados = cursor.fetchall()
                cursor.close()
                
                return True, resultados
                
        except Exception as e:
            return False, str(e)
    
    def consultar_nfe_por_fone(self, fone: str):
        """
        Consulta exata por telefone - retorna TODAS as NFes ordenadas por data mais recente
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT cpf_dest, nome_dest, fone, data_compra
                    FROM dim_nfe 
                    WHERE fone = %s
                    ORDER BY data_compra DESC, nome_dest
                    LIMIT 500
                """
                
                cursor.execute(query, (fone,))
                resultados = cursor.fetchall()
                cursor.close()
                
                return True, resultados
                
        except Exception as e:
            return False, str(e)
    
    def consultar_detalhes_compra(self, cpf: str, data_compra: str):
        """
        Busca detalhes completos de uma compra específica
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT nome_dest, cpf_dest, fone, ender_dest, num_dest, 
                           bairro, cep, municipio, uf, data_compra
                    FROM dim_nfe 
                    WHERE cpf_dest = %s AND data_compra = %s
                    LIMIT 1
                """
                
                cursor.execute(query, (cpf, data_compra))
                resultado = cursor.fetchall()
                cursor.close()
                
                return True, resultado
                
        except Exception as e:
            return False, str(e)

# Instância global
db_manager = DatabaseManager()