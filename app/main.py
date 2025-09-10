from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import sys

# Adicionar o diretório pai ao path para importar database.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import db_manager

# Criar aplicação FastAPI
app = FastAPI(
    title="extensao_seisp",
    description="Sistema de Consulta NFe - Consultas Exatas",
    version="2.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Página principal com formulário de consulta
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>extensao_seisp - Consulta NFe</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            .header { 
                background: linear-gradient(45deg, #2c3e50, #3498db);
                color: white; 
                padding: 30px; 
                text-align: center; 
            }
            .header h1 { font-size: 28px; margin-bottom: 10px; }
            .header p { opacity: 0.9; }
            .form-container { padding: 40px; }
            .form-group { margin-bottom: 25px; }
            .form-group label { 
                display: block; 
                margin-bottom: 8px; 
                font-weight: 600;
                color: #2c3e50;
            }
            .form-control { 
                width: 100%; 
                padding: 12px 15px; 
                border: 2px solid #ddd; 
                border-radius: 8px; 
                font-size: 16px;
                transition: border-color 0.3s;
            }
            .form-control:focus { 
                outline: none; 
                border-color: #3498db; 
                box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
            }
            .btn { 
                background: linear-gradient(45deg, #3498db, #2980b9);
                color: white; 
                padding: 12px 30px; 
                border: none; 
                border-radius: 8px; 
                font-size: 16px; 
                font-weight: 600;
                cursor: pointer; 
                transition: transform 0.2s;
                margin-right: 10px;
            }
            .btn:hover { transform: translateY(-2px); }
            .btn-secondary { 
                background: linear-gradient(45deg, #95a5a6, #7f8c8d);
            }
            .status { 
                background: #d4edda; 
                color: #155724;
                padding: 15px; 
                border-radius: 8px; 
                margin: 20px 0;
                border-left: 4px solid #28a745;
            }
            .results { 
                margin-top: 30px; 
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
            }
            .result-item {
                background: white;
                margin: 10px 0;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #3498db;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 extensao_seisp</h1>
                <p>Sistema de Consulta NFe - Consultas Exatas</p>
            </div>
            
            <div class="form-container">
                <div class="status">
                    <strong>✅ Fase 2 Concluída!</strong><br>
                    Sistema conectado ao banco PostgreSQL!
                </div>
                
                <form id="consultaForm">
                    <div class="form-group">
                        <label for="cpf">CPF do Destinatário:</label>
                        <input type="text" id="cpf" name="cpf" class="form-control" 
                               placeholder="Digite o CPF exato (ex: 12345678901)">
                    </div>
                    
                    <div class="form-group">
                        <label for="nome">Nome do Destinatário:</label>
                        <input type="text" id="nome" name="nome" class="form-control" 
                               placeholder="Digite o nome exato">
                    </div>
                    
                    <div class="form-group">
                        <label for="fone">Telefone:</label>
                        <input type="text" id="fone" name="fone" class="form-control" 
                               placeholder="Digite o telefone exato">
                    </div>
                    
                    <button type="button" onclick="consultar()" class="btn">🔍 Consultar</button>
                    <button type="button" onclick="limpar()" class="btn btn-secondary">🧹 Limpar</button>
                    <button type="button" onclick="testarConexao()" class="btn btn-secondary">🔌 Testar Conexão</button>
                </form>
                
                <div id="resultados" class="results" style="display: none;">
                    <h3>📊 Resultados:</h3>
                    <div id="listaResultados"></div>
                </div>
            </div>
        </div>
        
        <script>
            async function consultar() {
                const cpf = document.getElementById('cpf').value;
                const nome = document.getElementById('nome').value;
                const fone = document.getElementById('fone').value;
                
                if (!cpf && !nome && !fone) {
                    alert('Preencha pelo menos um campo para consulta!');
                    return;
                }
                
                let url = '/consultar?';
                if (cpf) url += `cpf=${encodeURIComponent(cpf)}&`;
                if (nome) url += `nome=${encodeURIComponent(nome)}&`;
                if (fone) url += `fone=${encodeURIComponent(fone)}&`;
                
                try {
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    mostrarResultados(data);
                } catch (error) {
                    alert('Erro ao consultar: ' + error.message);
                }
            }
            
            function mostrarResultados(data) {
                const resultadosDiv = document.getElementById('resultados');
                const listaDiv = document.getElementById('listaResultados');
                
                if (data.success && data.resultados.length > 0) {
                    let html = '';
                    data.resultados.forEach(item => {
                        html += `
                            <div class="result-item">
                                <strong>CPF:</strong> ${item.cpf_dest || 'N/A'}<br>
                                <strong>Nome:</strong> ${item.nome_dest || 'N/A'}<br>
                                <strong>Telefone:</strong> ${item.fone || 'N/A'}
                            </div>
                        `;
                    });
                    listaDiv.innerHTML = html;
                    resultadosDiv.style.display = 'block';
                } else if (data.success && data.resultados.length === 0) {
                    listaDiv.innerHTML = '<p>❌ Nenhum resultado encontrado.</p>';
                    resultadosDiv.style.display = 'block';
                } else {
                    alert('Erro: ' + data.error);
                }
            }
            
            function limpar() {
                document.getElementById('cpf').value = '';
                document.getElementById('nome').value = '';
                document.getElementById('fone').value = '';
                document.getElementById('resultados').style.display = 'none';
            }
            
            async function testarConexao() {
                try {
                    const response = await fetch('/test-db');
                    const data = await response.json();
                    
                    if (data.success) {
                        alert('✅ Conexão OK!\\n' + data.version);
                    } else {
                        alert('❌ Erro na conexão:\\n' + data.error);
                    }
                } catch (error) {
                    alert('❌ Erro: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/consultar")
async def consultar_nfe(cpf: str = None, nome: str = None, fone: str = None):
    """
    Endpoint para consultar NFe por CPF, nome ou telefone (consultas exatas)
    """
    try:
        resultados = []
        
        if cpf:
            success, data = db_manager.consultar_nfe_por_cpf(cpf)
            if success:
                resultados.extend(data)
            else:
                raise HTTPException(status_code=500, detail=f"Erro na consulta por CPF: {data}")
        
        if nome:
            success, data = db_manager.consultar_nfe_por_nome(nome)
            if success:
                resultados.extend(data)
            else:
                raise HTTPException(status_code=500, detail=f"Erro na consulta por nome: {data}")
        
        if fone:
            success, data = db_manager.consultar_nfe_por_fone(fone)
            if success:
                resultados.extend(data)
            else:
                raise HTTPException(status_code=500, detail=f"Erro na consulta por telefone: {data}")
        
        # Remove duplicatas
        resultados_unicos = []
        cpfs_vistos = set()
        for item in resultados:
            cpf_item = item.get('cpf_dest')
            if cpf_item and cpf_item not in cpfs_vistos:
                cpfs_vistos.add(cpf_item)
                resultados_unicos.append(dict(item))
        
        return {
            "success": True,
            "total": len(resultados_unicos),
            "resultados": resultados_unicos
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/test-db")
async def test_database():
    """
    Testa a conexão com o banco de dados
    """
    success, result = db_manager.test_connection()
    
    if success:
        return {
            "success": True,
            "message": "Conexão OK!",
            "version": result
        }
    else:
        return {
            "success": False,
            "error": result
        }

if __name__ == "__main__":
    print("🚀 Iniciando extensao_seisp - Fase 2")
    print("📊 Consultas exatas na tabela dim_nfe")
    print("🌐 Acesse: http://127.0.0.1:8000")
    print("❌ Para parar: Ctrl+C")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )