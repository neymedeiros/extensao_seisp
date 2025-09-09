from database import DatabaseConnection

class ExploradorTabelas:
    """
    Classe para explorar as tabelas e estrutura do banco
    """
    
    def __init__(self):
        self.db = DatabaseConnection()
    
    def listar_tabelas(self):
        """
        Lista todas as tabelas do schema atual
        """
        if not self.db.conectar():
            return
        
        try:
            cursor = self.db.connection.cursor()
            
            # Query para listar tabelas do schema
            query = """
                SELECT table_name, table_type
                FROM information_schema.tables 
                WHERE table_schema = %s
                ORDER BY table_name;
            """
            
            cursor.execute(query, (self.db.schema,))
            tabelas = cursor.fetchall()
            
            print(f"\n📋 Tabelas encontradas no schema '{self.db.schema}':")
            print("-" * 60)
            
            for tabela in tabelas:
                tipo = "📊" if tabela['table_type'] == 'BASE TABLE' else "👁️"
                print(f"{tipo} {tabela['table_name']} ({tabela['table_type']})")
            
            print(f"\n✅ Total: {len(tabelas)} tabelas encontradas")
            cursor.close()
            
        except Exception as erro:
            print(f"❌ Erro ao listar tabelas: {erro}")
        
        finally:
            self.db.desconectar()
    
    def buscar_tabelas_nota_fiscal(self):
        """
        Busca tabelas que podem estar relacionadas a notas fiscais
        """
        if not self.db.conectar():
            return
        
        try:
            cursor = self.db.connection.cursor()
            
            # Busca tabelas com nomes relacionados a nota fiscal
            query = """
                SELECT table_name, table_type
                FROM information_schema.tables 
                WHERE table_schema = %s
                AND (
                    LOWER(table_name) LIKE '%nota%'
                    OR LOWER(table_name) LIKE '%fiscal%'
                    OR LOWER(table_name) LIKE '%nf%'
                    OR LOWER(table_name) LIKE '%pessoa%'
                    OR LOWER(table_name) LIKE '%compra%'
                    OR LOWER(table_name) LIKE '%cliente%'
                    OR LOWER(table_name) LIKE '%fornecedor%'
                )
                ORDER BY table_name;
            """
            
            cursor.execute(query, (self.db.schema,))
            tabelas = cursor.fetchall()
            
            print(f"\n🔍 Tabelas relacionadas a notas fiscais:")
            print("-" * 60)
            
            if tabelas:
                for tabela in tabelas:
                    print(f"📊 {tabela['table_name']}")
            else:
                print("❌ Nenhuma tabela com nome relacionado encontrada")
                print("💡 Vamos listar todas as tabelas para você escolher")
            
            cursor.close()
            return len(tabelas) > 0
            
        except Exception as erro:
            print(f"❌ Erro ao buscar tabelas: {erro}")
            return False
        
        finally:
            self.db.desconectar()
    
    def descrever_tabela(self, nome_tabela):
        """
        Mostra a estrutura de uma tabela específica
        """
        if not self.db.conectar():
            return
        
        try:
            cursor = self.db.connection.cursor()
            
            # Query para descrever a estrutura da tabela
            query = """
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    character_maximum_length
                FROM information_schema.columns 
                WHERE table_schema = %s 
                AND table_name = %s
                ORDER BY ordinal_position;
            """
            
            cursor.execute(query, (self.db.schema, nome_tabela))
            colunas = cursor.fetchall()
            
            print(f"\n📋 Estrutura da tabela '{nome_tabela}':")
            print("-" * 80)
            print(f"{'COLUNA':<25} {'TIPO':<20} {'NULO':<8} {'TAMANHO':<10}")
            print("-" * 80)
            
            for coluna in colunas:
                nome = coluna['column_name']
                tipo = coluna['data_type']
                nulo = "SIM" if coluna['is_nullable'] == 'YES' else "NÃO"
                tamanho = coluna['character_maximum_length'] or '-'
                
                print(f"{nome:<25} {tipo:<20} {nulo:<8} {tamanho}")
            
            print(f"\n✅ Total: {len(colunas)} colunas")
            cursor.close()
            
        except Exception as erro:
            print(f"❌ Erro ao descrever tabela: {erro}")
        
        finally:
            self.db.desconectar()

# Exemplo de uso
if __name__ == "__main__":
    explorador = ExploradorTabelas()
    
    print("🚀 Explorando o banco de dados...")
    
    # Primeiro, busca tabelas relacionadas a notas fiscais
    encontrou_tabelas_nf = explorador.buscar_tabelas_nota_fiscal()
    
    # Se não encontrou tabelas específicas, lista todas
    if not encontrou_tabelas_nf:
        explorador.listar_tabelas()
    
    print("\n" + "="*60)
    print("💡 Próximos passos:")
    print("1. Identifique suas tabelas de nota fiscal, pessoa e compra")
    print("2. Use: explorador.descrever_tabela('nome_da_tabela')")
    print("3. Vamos criar as consultas!")