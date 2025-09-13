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
            .results-header {
                background: linear-gradient(45deg, #28a745, #20c997);
                color: white;
                padding: 15px 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                font-size: 18px;
                font-weight: 600;
                text-align: center;
            }
            .result-item {
                background: white;
                margin: 15px 0;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #3498db;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .result-item:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            }
            .result-info {
                display: flex;
                justify-content: space-between;
                margin-bottom: 15px;
            }
            .info-column {
                flex: 1;
                margin-right: 20px;
            }
            .result-actions {
                text-align: right;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #eee;
            }
            .btn-view {
                background: linear-gradient(45deg, #e74c3c, #c0392b);
                color: white;
                padding: 8px 20px;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .btn-view:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
            }
            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.5);
                animation: fadeIn 0.3s;
            }
            .modal-content {
                background-color: white;
                margin: 5% auto;
                padding: 0;
                border-radius: 15px;
                width: 90%;
                max-width: 800px;
                max-height: 85vh;
                overflow-y: auto;
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                animation: slideIn 0.3s;
            }
            .modal-header {
                background: linear-gradient(45deg, #e74c3c, #c0392b);
                color: white;
                padding: 20px 30px;
                border-radius: 15px 15px 0 0;
                position: relative;
            }
            .modal-header h2 {
                margin: 0;
                font-size: 24px;
            }
            .close {
                position: absolute;
                right: 20px;
                top: 15px;
                color: white;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
                width: 35px;
                height: 35px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background-color 0.2s;
            }
            .close:hover {
                background-color: rgba(255,255,255,0.2);
            }
            .modal-body {
                padding: 30px;
            }
            .detail-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 20px;
            }
            .detail-item {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #e74c3c;
            }
            .detail-label {
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            .detail-value {
                color: #34495e;
                font-size: 16px;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideIn {
                from { transform: translateY(-50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @media (max-width: 768px) {
                .detail-grid {
                    grid-template-columns: 1fr;
                }
                .result-info {
                    flex-direction: column;
                }
                .info-column {
                    margin-right: 0;
                    margin-bottom: 10px;
                }
            }
            .no-results {
                text-align: center;
                padding: 40px;
                color: #666;
                font-size: 18px;
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
                    <div id="resultsHeader" class="results-header"></div>
                    <div id="listaResultados"></div>
                </div>
            </div>
        </div>
        
        <!-- Modal de Visualização da Compra -->
        <div id="modalCompra" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>🛍️ Detalhes da Compra</h2>
                    <span class="close" onclick="fecharModal()">&times;</span>
                </div>
                <div class="modal-body">
                    <div id="detalhesCompra">
                        <!-- Conteúdo será carregado dinamicamente -->
                    </div>
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
                const headerDiv = document.getElementById('resultsHeader');
                const listaDiv = document.getElementById('listaResultados');
                
                if (data.success && data.resultados.length > 0) {
                    // Mostrar header com total de registros
                    headerDiv.innerHTML = `📊 ${data.total} registro(s) encontrado(s)`;
                    
                    let html = '';
                    data.resultados.forEach((item, index) => {
                        html += `
                            <div class="result-item">
                                <div style="color: #666; font-size: 14px; margin-bottom: 10px;">
                                    <strong>Registro ${index + 1}</strong>
                                </div>
                                <div class="result-info">
                                    <div class="info-column">
                                        <strong>CPF:</strong> ${item.cpf_dest || 'N/A'}<br>
                                        <strong>Nome:</strong> ${item.nome_dest || 'N/A'}
                                    </div>
                                    <div class="info-column">
                                        <strong>Telefone:</strong> ${item.fone || 'N/A'}<br>
                                        <strong>Data:</strong> ${item.data_compra || 'N/A'}
                                    </div>
                                </div>
                                <div class="result-actions">
                                    <button class="btn-view" onclick="visualizarCompra('${item.cpf_dest}', '${item.data_compra}', ${index})">
                                        👁️ Visualizar Compra
                                    </button>
                                </div>
                            </div>
                        `;
                    });
                    listaDiv.innerHTML = html;
                    resultadosDiv.style.display = 'block';
                } else if (data.success && data.resultados.length === 0) {
                    headerDiv.innerHTML = `📊 0 registros encontrados`;
                    listaDiv.innerHTML = '<div class="no-results">⚠️ Nenhum resultado encontrado.</div>';
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
            
            async function visualizarCompra(cpf, data, index) {
                try {
                    const response = await fetch(`/detalhes-compra?cpf=${encodeURIComponent(cpf)}&data=${encodeURIComponent(data)}`);
                    const dados = await response.json();
                    
                    if (dados.success && dados.detalhes) {
                        mostrarModalCompra(dados.detalhes, index + 1);
                    } else {
                        alert('❌ Erro ao carregar detalhes: ' + (dados.error || 'Dados não encontrados'));
                    }
                } catch (error) {
                    alert('❌ Erro: ' + error.message);
                }
            }
            
            function mostrarModalCompra(detalhes, numeroRegistro) {
                const detalhesDiv = document.getElementById('detalhesCompra');
                
                detalhesDiv.innerHTML = `
                    <div style="text-align: center; margin-bottom: 20px; padding: 15px; background: #e8f5e8; border-radius: 8px;">
                        <strong style="color: #28a745; font-size: 18px;">📋 Registro ${numeroRegistro}</strong>
                    </div>
                    
                    <div class="detail-grid">
                        <div class="detail-item">
                            <div class="detail-label">👤 Nome do Destinatário</div>
                            <div class="detail-value">${detalhes.nome_dest || 'N/A'}</div>
                        </div>
                        
                        <div class="detail-item">
                            <div class="detail-label">🆔 CPF</div>
                            <div class="detail-value">${detalhes.cpf_dest || 'N/A'}</div>
                        </div>
                        
                        <div class="detail-item">
                            <div class="detail-label">📞 Telefone</div>
                            <div class="detail-value">${detalhes.fone || 'N/A'}</div>
                        </div>
                        
                        <div class="detail-item">
                            <div class="detail-label">📅 Data da Compra</div>
                            <div class="detail-value">${detalhes.data_compra || 'N/A'}</div>
                        </div>
                        
                        <div class="detail-item">
                            <div class="detail-label">🏠 Endereço</div>
                            <div class="detail-value">${detalhes.ender_dest || 'N/A'}</div>
                        </div>
                        
                        <div class="detail-item">
                            <div class="detail-label">🔢 Número</div>
                            <div class="detail-value">${detalhes.num_dest || 'N/A'}</div>
                        </div>
                        
                        <div class="detail-item">
                            <div class="detail-label">🏘️ Bairro</div>
                            <div class="detail-value">${detalhes.bairro || 'N/A'}</div>
                        </div>
                        
                        <div class="detail-item">
                            <div class="detail-label">📮 CEP</div>
                            <div class="detail-value">${detalhes.cep || 'N/A'}</div>
                        </div>
                        
                        <div class="detail-item">
                            <div class="detail-label">🏙️ Município</div>
                            <div class="detail-value">${detalhes.municipio || 'N/A'}</div>
                        </div>
                        
                        <div class="detail-item">
                            <div class="detail-label">🗺️ UF</div>
                            <div class="detail-value">${detalhes.uf || 'N/A'}</div>
                        </div>
                    </div>
                `;
                
                document.getElementById('modalCompra').style.display = 'block';
            }
            
            function fecharModal() {
                document.getElementById('modalCompra').style.display = 'none';
            }
            
            // Fechar modal clicando fora dele
            window.onclick = function(event) {
                const modal = document.getElementById('modalCompra');
                if (event.target === modal) {
                    fecharModal();
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
        
        # Converter para lista de dicionários (mantém todos os registros)
        resultados_lista = [dict(item) for item in resultados]
        
        return {
            "success": True,
            "total": len(resultados_lista),
            "resultados": resultados_lista
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/detalhes-compra")
async def detalhes_compra(cpf: str, data: str):
    """
    Endpoint para buscar detalhes completos de uma compra específica
    """
    try:
        success, resultado = db_manager.consultar_detalhes_compra(cpf, data)
        
        if success and resultado:
            return {
                "success": True,
                "detalhes": dict(resultado[0]) if resultado else None
            }
        else:
            return {
                "success": False,
                "error": "Detalhes não encontrados"
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
    print("⛔ Para parar: Ctrl+C")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )