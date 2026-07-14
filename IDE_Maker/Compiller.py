from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import subprocess
import tempfile
import os
import sys
import json
import traceback
import shutil
from datetime import datetime
import PyInstaller.__main__
import threading
import time
import socket

app = Flask(__name__)
CORS(app)

# ============================================
# CONFIGURAÇÕES
# ============================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PASTA_EXECUTAVEIS = os.path.join(BASE_DIR, 'compilados')
os.makedirs(PASTA_EXECUTAVEIS, exist_ok=True)

PASTA_TEMP = os.path.join(BASE_DIR, 'temp')
os.makedirs(PASTA_TEMP, exist_ok=True)

PASTA_LOGS = os.path.join(BASE_DIR, 'logs')
os.makedirs(PASTA_LOGS, exist_ok=True)

# ============================================
# HTML COMPLETO EMBUTIDO (DENTRO DO CÓDIGO)
# ============================================

HTML_PAGINA = '''
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GuiSpark Designer</title>
    <link rel="stylesheet" href="Assets/Graphic.css">
    <link rel="stylesheet" href="Assets/Editor.css">
</head>
<body>
    <div class="container">
        <div class="IDE_Container">
            <div class="TOP_Container">
                <div class="TopNav">
                    <select id="File">
                        <option value="" id="f">Arquivo</option>
                        <option value="New" id="n">Nova Interface</option>
                        <option value="Open" id="o">Abrir</option>
                        <option value="Save" id="s">Salvar</option>
                        <option value="Close" id="c">Fechar</option>
                    </select>
                    
                    <button value="Compile" id="C">Compilar</button>
                    <button value="Execute" id="e">Executar</button>
                    <button id="deleteWidget">Excluir elemento</button>
                    <button id="btnVisualMode">Modo Texto</button>
                    <button id="btnGraphicMode">Modo Gráfico</button>
                    
                    <select id="Languages">
                        <option value="Pt">Português</option>
                        <option value="En">English</option>
                        <option value="Es">Español</option>
                    </select>
                </div>
                <div id="GraphicalPallete">
                    <img src="Assets/Graphics/slider.svg" draggable="true" class="tool" data-widget="slider">
                    <img src="Assets/Graphics/checkbox.svg" draggable="true" class="tool" data-widget="checkbox">
                    <img src="Assets/Graphics/Label.svg" draggable="true" class="tool" data-widget="label">
                    <img src="Assets/Graphics/input-field.svg" draggable="true" class="tool" data-widget="entry">
                    <img src="Assets/Graphics/progressbar.svg" draggable="true" class="tool" data-widget="progress">
                    <img src="Assets/Graphics/combobox.svg" draggable="true" class="tool" data-widget="combobox">
                    <img src="Assets/Graphics/web.svg" draggable="true" class="tool" data-widget="web">
                    <img src="Assets/Graphics/Pannel.svg" draggable="true" class="tool" data-widget="frame">
                    <img src="Assets/Graphics/button.svg" draggable="true" class="tool" data-widget="button">
                </div>
            </div>
            <div class="Propperties">
                <table>
                    <tr>
                        <th>Propriedade</th>
                        <th>Valor</th>
                    </tr>
                    <tr>
                        <td>Titulo</td>
                        <td><input type="text" id="WTitle" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>x</td>
                        <td><input type="number" id="x" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>y</td>
                        <td><input type="number" id="y" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>width</td>
                        <td><input type="number" id="width" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>height</td>
                        <td><input type="number" id="height" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>text</td>
                        <td><input type="text" id="text" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>bg</td>
                        <td><input type="text" id="bg" onchange="atualizarWidget()" placeholder="#ffffff"></td>
                    </tr>
                    <tr>
                        <td>fg</td>
                        <td><input type="text" id="fg" onchange="atualizarWidget()" placeholder="#000000"></td>
                    </tr>
                    <tr>
                        <td>hover_bg</td>
                        <td><input type="text" id="hover_bg" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>pressed_bg</td>
                        <td><input type="text" id="pressed_bg" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>border_radius</td>
                        <td><input type="number" id="border_radius" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>command</td>
                        <td><input type="text" id="command" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>placeholder</td>
                        <td><input type="text" id="placeholder" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>min_value</td>
                        <td><input type="number" id="min_value" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>max_value</td>
                        <td><input type="number" id="max_value" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>url</td>
                        <td><input type="text" id="url" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>value</td>
                        <td><input type="text" id="value" onchange="atualizarWidget()"></td>
                    </tr>
                    <tr>
                        <td>items</td>
                        <td><input type="text" id="items" onchange="atualizarWidget()" placeholder="item1,item2,item3"></td>
                    </tr>
                    <tr>
                        <td>orientation</td>
                        <td>
                            <select id="orientation" onchange="atualizarWidget()">
                                <option value="horizontal">horizontal</option>
                                <option value="vertical">vertical</option>
                            </select>
                        </td>
                    </tr>
                </table>
            </div>
            <div class="GraphAndTextArea">
                <div id="modoVisual">
                    <div id="canvas"></div>
                </div>
                <div id="modoTexto" style="display:none;">
                    <textarea id="codigoEditor" spellcheck="false"></textarea>
                </div>
            </div>
        </div>
    </div>
    <script src="Assets/Graphic.js"></script>
    <script src="Assets/CodeGenerator.js"></script>
    <script src="Assets/PythonParser.js"></script>
    <script src="Assets/DragDrop.js"></script>
    <script src="Assets/Editor.js"></script>
</body>
</html>

'''

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def registrar_log(mensagem, tipo='info'):
    try:
        log_path = os.path.join(PASTA_LOGS, f"compilacoes_{datetime.now().strftime('%Y%m%d')}.log")
        with open(log_path, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] [{tipo.upper()}] {mensagem}\n")
    except:
        pass

def salvar_codigo_para_compilar(codigo, filename, metadata):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome_base = os.path.splitext(filename)[0]
    nome_base = "".join(c for c in nome_base if c.isalnum() or c in " _-")
    nome_arquivo = f"{nome_base}_{timestamp}.py"
    caminho_py = os.path.join(PASTA_EXECUTAVEIS, nome_arquivo)
    
    codigo_ajustado = f"""import sys
import os

if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication

def obter_tamanho_tela(percentual=0.95):
    try:
        app_temp = QApplication.instance() or QApplication(sys.argv)
        screen = app_temp.primaryScreen()
        size = screen.size()
        return int(size.width() * percentual), int(size.height() * percentual)
    except:
        return 1280, 720

LARGURA_TELA, ALTURA_TELA = obter_tamanho_tela(0.95)

{codigo}
"""
    
    with open(caminho_py, 'w', encoding='utf-8') as f:
        f.write(f"# ============================================\n")
        f.write(f"# Compilado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"# Título: {metadata.get('title', 'Sem título')}\n")
        f.write(f"# ============================================\n\n")
        f.write(codigo_ajustado)
    
    return caminho_py, nome_arquivo

def gerar_exe(caminho_py, nome_base):
    try:
        nome_exe = f"{nome_base}.exe"
        caminho_exe = os.path.join(PASTA_EXECUTAVEIS, nome_exe)
        
        if os.path.exists(caminho_exe):
            os.remove(caminho_exe)
        
        pyinstaller_args = [
            '--onefile',
            '--noconsole',
            '--distpath', PASTA_EXECUTAVEIS,
            '--workpath', os.path.join(PASTA_TEMP, 'build'),
            '--specpath', os.path.join(PASTA_TEMP, 'spec'),
            '--name', nome_base,
            '--add-data', f"{os.path.join(BASE_DIR, 'Assets')};Assets",
            '--exclude-module', 'tkinter',
            '--exclude-module', 'matplotlib',
            '--exclude-module', 'numpy',
            '--exclude-module', 'pandas',
            '--exclude-module', 'PIL',
            '--exclude-module', 'cryptography',
            '--exclude-module', 'test',
            '--exclude-module', 'unittest',
            '--exclude-module', 'pydoc',
            '--exclude-module', 'doctest',
            '--hidden-import', 'BetterGuiSpark',
            caminho_py
        ]
        
        print(f" Gerando .exe: {nome_exe}")
        PyInstaller.__main__.run(pyinstaller_args)
        
        if os.path.exists(caminho_exe):
            print(f" .exe criado: {caminho_exe}")
            return caminho_exe, nome_exe
        
        return None, None
            
    except Exception as e:
        print(f" Erro ao gerar .exe: {e}")
        return None, None

def limpar_arquivos_temporarios(caminho_py, nome_base):
    try:
        if os.path.exists(caminho_py):
            os.remove(caminho_py)
            print(f" .py removido: {caminho_py}")
        
        build_path = os.path.join(PASTA_TEMP, 'build')
        spec_path = os.path.join(PASTA_TEMP, 'spec')
        
        if os.path.exists(build_path):
            shutil.rmtree(build_path)
        if os.path.exists(spec_path):
            shutil.rmtree(spec_path)
            
    except Exception as e:
        print(f" Erro ao limpar: {e}")

def executar_codigo_temp(codigo, timeout=30):
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8', dir=PASTA_TEMP) as f:
            codigo_ajustado = f"""import sys
import os

if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication

def obter_tamanho_tela(percentual=0.95):
    try:
        app_temp = QApplication.instance() or QApplication(sys.argv)
        screen = app_temp.primaryScreen()
        size = screen.size()
        return int(size.width() * percentual), int(size.height() * percentual)
    except:
        return 1280, 720

LARGURA_TELA, ALTURA_TELA = obter_tamanho_tela(0.95)

{codigo}
"""
            f.write(codigo_ajustado)
            temp_file = f.name
        
        print(f" Arquivo temporário: {temp_file}")
        
        env = os.environ.copy()
        env['PYTHONPATH'] = BASE_DIR + os.pathsep + env.get('PYTHONPATH', '')
        
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=BASE_DIR,
            env=env
        )
        
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except:
                pass
        
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'success': result.returncode == 0
        }
        
    except subprocess.TimeoutExpired:
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except:
                pass
        return {
            'stdout': '',
            'stderr': f' Timeout ({timeout}s)',
            'returncode': -1,
            'success': False
        }
    except Exception as e:
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except:
                pass
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': -1,
            'success': False
        }

def verificar_se_servidor_esta_rodando(host='127.0.0.1', port=5000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        resultado = sock.connect_ex((host, port))
        sock.close()
        return resultado == 0
    except:
        return False



# ============================================
# ROTAS
# ============================================

@app.route('/')
def index():
    """Retorna o HTML embutido"""
    return HTML_PAGINA

@app.route('/Assets/<path:path>')
def serve_assets(path):
    """Serve arquivos da pasta Assets"""
    return send_from_directory('Assets', path)

@app.route('/compile', methods=['POST', 'OPTIONS'])
def compilar():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({'success': False, 'error': 'Código não fornecido'}), 400
        
        codigo = data['code']
        filename = data.get('filename', 'script.py')
        metadata = data.get('metadata', {})
        
        print(f"\n{'='*50}")
        print(f" Compilando: {filename}")
        print(f" Tamanho: {len(codigo)} caracteres")
        print(f"{'='*50}\n")
        
        caminho_py, nome_arquivo = salvar_codigo_para_compilar(codigo, filename, metadata)
        nome_base = os.path.splitext(nome_arquivo)[0]
        print(f" .py salvo: {caminho_py}")
        
        print(" Gerando .exe (isso pode levar alguns minutos)...")
        caminho_exe, nome_exe = gerar_exe(caminho_py, nome_base)
        
        if not caminho_exe or not os.path.exists(caminho_exe):
            if os.path.exists(caminho_py):
                os.remove(caminho_py)
            return jsonify({
                'success': False,
                'error': 'Erro ao gerar .exe',
                'message': 'Falha na compilação. Verifique o código.'
            }), 500
        
        limpar_arquivos_temporarios(caminho_py, nome_base)
        
        tamanho = os.path.getsize(caminho_exe)
        registrar_log(f"Compilado: {filename} → {nome_exe} | Tamanho: {tamanho} bytes")
        
        return jsonify({
            'success': True,
            'executable': nome_exe,
            'executable_path': caminho_exe,
            'size': tamanho,
            'message': f' Compilado! {nome_exe} criado.',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        erro_msg = str(e)
        print(f" Erro: {traceback.format_exc()}")
        registrar_log(f"ERRO: {erro_msg}", 'error')
        return jsonify({'success': False, 'error': erro_msg}), 500

@app.route('/execute', methods=['POST', 'OPTIONS'])
def executar():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json()
        
        if not data or 'code' not in data:
            return jsonify({'success': False, 'error': 'Código não fornecido'}), 400
        
        codigo = data['code']
        filename = data.get('filename', 'script.py')
        timeout = data.get('timeout', 30)
        
        print(f"\n{'='*50}")
        print(f" Executando: {filename}")
        print(f" Tamanho: {len(codigo)} caracteres")
        print(f" Timeout: {timeout}s")
        print(f"{'='*50}\n")
        
        resultado = executar_codigo_temp(codigo, timeout)
        
        if resultado['success']:
            registrar_log(f"Executado: {filename} | Saída: {len(resultado['stdout'])} caracteres")
        else:
            registrar_log(f"Erro: {filename} | {resultado['stderr'][:100]}", 'error')
        
        return jsonify({
            'success': resultado['success'],
            'output': resultado['stdout'],
            'error': resultado['stderr'] if not resultado['success'] else None,
            'returncode': resultado['returncode'],
            'message': ' Executado!' if resultado['success'] else '❌ Erro',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        erro_msg = str(e)
        print(f" Erro: {traceback.format_exc()}")
        registrar_log(f"ERRO: {erro_msg}", 'error')
        return jsonify({'success': False, 'error': erro_msg}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'base_dir': BASE_DIR,
        'executaveis': len([f for f in os.listdir(PASTA_EXECUTAVEIS) if f.endswith('.exe')])
    })

@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        print(" Servidor desligando...")
        registrar_log("Servidor desligado via API", 'info')
        os._exit(0)
        return jsonify({'success': True, 'message': 'Servidor desligado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    print("=" * 60)
    print(" GUISPARK MAKER v2.0")
    print("=" * 60)
    
    if verificar_se_servidor_esta_rodando():
        print(" Servidor já está rodando!")
        print(" Abrindo navegador...")
        sys.exit(0)
    
    print(f" Base: {BASE_DIR}")
    print(f" Executáveis: {PASTA_EXECUTAVEIS}")
    print("=" * 60)
    print(" Servidor Web: http://localhost:5000")
    print(" Endpoints:")
    print("   GET  /              - Interface GUI")
    print("   POST /compile      - Compilar para .exe")
    print("   POST /execute      - Executar código")
    print("   GET  /health       - Status")
    print("   POST /shutdown     - Desligar servidor")
    print("=" * 60)
    print(" PRODUCTION MODE")
    print(" HTML embutido no .exe!")
    print(" A primeira compilação pode demorar alguns minutos!")
    print("=" * 60)
    
    
    try:
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n Servidor interrompido")
        sys.exit(0)