from BetterGuiSpark import GuiSpark
import os
import sys
import subprocess
import importlib
import socket
import ctypes
import platform
import time
import shutil
import urllib.request

class Diagnosticador:
    def __init__(self):
        self.problemas = []
        self.solucoes = []
        self.corrigidos = []
        self.gui = None
        self.verificacao_atual = ""
        self.icone_status = "🔄"
        
        # Widgets
        self.progress_bar = None
        self.status_label = None
        self.log_text = None
        self.resultado_label = None
        self.btn_corrigir = None
        self.btn_abrir = None
        self.btn_sair = None
        self.frame_status = None
        self.label_icone = None
        self.label_verificacao = None
        self.label_porcentagem = None
        
    def criar_interface(self):
        """Cria a interface de diagnóstico interativa"""
        
        self.gui = GuiSpark(
            title="🔧 GuiMaker-Problem Solver",
            width=500,
            height=550
        )
        
        self.gui.set_theme("dark")
        
        # Título
        self.gui.add_widget(
            "label",
            x=20,
            y=10,
            width=460,
            height=35,
            text="🔧 Verificador do Sistema",
            bg="",
            fg="#af72fa",
            border_radius=0,
            command=None
        )
        
        # Subtítulo
        self.gui.add_widget(
            "label",
            x=20,
            y=45,
            width=460,
            height=20,
            text="Diagnóstico e correção automática",
            bg="",
            fg="#888888",
            border_radius=0,
            command=None
        )
        
        # Frame de status
        self.frame_status = self.gui.add_widget(
            "frame",
            x=20,
            y=75,
            width=460,
            height=55,
            text="",
            bg="#2b2b2b",
            fg="",
            border_radius=8,
            command=None
        )
        
        self.label_icone = self.gui.add_widget(
            "label",
            x=35,
            y=88,
            width=40,
            height=30,
            text="⏳",
            bg="",
            fg="#af72fa",
            border_radius=0,
            command=None
        )
        
        self.label_verificacao = self.gui.add_widget(
            "label",
            x=85,
            y=88,
            width=370,
            height=30,
            text="Iniciando diagnóstico...",
            bg="",
            fg="#ffffff",
            border_radius=0,
            command=None
        )
        
        # Barra de progresso
        self.label_porcentagem = self.gui.add_widget(
            "label",
            x=20,
            y=138,
            width=460,
            height=20,
            text="0%",
            bg="",
            fg="#af72fa",
            border_radius=0,
            command=None
        )
        
        self.progress_bar = self.gui.add_widget(
            "progress",
            x=20,
            y=160,
            width=460,
            height=25,
            text="",
            bg="",
            fg="",
            border_radius=0,
            command=None,
            min_value=0,
            max_value=100,
            value=0
        )
        
        # Frame do log
        frame_log = self.gui.add_widget(
            "frame",
            x=20,
            y=195,
            width=460,
            height=200,
            text="",
            bg="#1e1e1e",
            fg="",
            border_radius=6,
            command=None
        )
        
        self.gui.add_widget(
            "label",
            x=30,
            y=203,
            width=440,
            height=20,
            text="📋 Log em tempo real",
            bg="",
            fg="#af72fa",
            border_radius=0,
            command=None
        )
        
        self.log_text = self.gui.add_widget(
            "text",
            x=30,
            y=228,
            width=440,
            height=155,
            text="⏳ Aguardando início...\n",
            bg="#0d0d0d",
            fg="#d4d4d4",
            border_radius=4,
            command=None,
            placeholder="Log em tempo real"
        )
        
        # Resultado final
        self.resultado_label = self.gui.add_widget(
            "label",
            x=20,
            y=405,
            width=460,
            height=40,
            text="",
            bg="#2b2b2b",
            fg="#ffffff",
            border_radius=6,
            command=None
        )
        
        # Botões
        self.btn_corrigir = self.gui.add_widget(
            "button",
            x=20,
            y=455,
            width=140,
            height=40,
            text="🔧 Corrigir",
            bg="#f39c12",
            fg="#000000",
            hover_bg="#d68910",
            pressed_bg="#b9770e",
            border_radius=6,
            command=self.corrigir_problemas
        )
        
        self.btn_abrir = self.gui.add_widget(
            "button",
            x=175,
            y=455,
            width=140,
            height=40,
            text="🚀 Iniciar",
            bg="#2ecc71",
            fg="#000000",
            hover_bg="#27ae60",
            pressed_bg="#1e8449",
            border_radius=6,
            command=self.abrir_programa
        )
        
        self.btn_sair = self.gui.add_widget(
            "button",
            x=330,
            y=455,
            width=150,
            height=40,
            text="❌ Sair",
            bg="#e74c3c",
            fg="#ffffff",
            hover_bg="#c0392b",
            pressed_bg="#a93226",
            border_radius=6,
            command=self.sair
        )
        
        self.gui.set_widget_enabled(self.btn_corrigir, False)
        self.gui.set_widget_enabled(self.btn_abrir, False)
        
        self.gui.set_timer(500, self.diagnosticar, repeat=False)
        
    def log(self, mensagem, tipo="info", emoji=""):
        """Adiciona mensagem ao log em tempo real"""
        cores = {
            "info": "#3498db",
            "sucesso": "#2ecc71",
            "alerta": "#f39c12",
            "erro": "#e74c3c",
            "destaque": "#af72fa",
            "correcao": "#1abc9c"
        }
        cor = cores.get(tipo, "#ffffff")
        
        texto_atual = self.gui.get_widget_text(self.log_text) or ""
        linhas = texto_atual.split('\n')
        if len(linhas) > 35:
            texto_atual = '\n'.join(linhas[-30:])
        
        self.gui.set_widget_text(
            self.log_text, 
            texto_atual + f'{emoji}{mensagem}\n'
        )
        self.gui.refresh()
        
    def atualizar_status(self, mensagem, icone="⏳", progresso=None):
        """Atualiza o status em tempo real"""
        self.gui.set_widget_text(self.label_icone, icone)
        self.gui.set_widget_text(self.label_verificacao, mensagem)
        
        if progresso is not None:
            self.gui.set_widget_text(self.progress_bar, progresso)
            self.gui.set_widget_text(self.label_porcentagem, f"{progresso}%")
            
        self.gui.refresh()
        
    def diagnosticar(self):
        """Executa diagnóstico completo em tempo real"""
        
        # PASSO 1: VERIFICANDO ASSETS
        self.log("🔍 Iniciando diagnóstico do sistema...", "destaque", "🔍")
        self.atualizar_status("Verificando estrutura de pastas...", "📁", 0)
        time.sleep(0.3)
        self.verificar_assets()
        self.gui.refresh()
        time.sleep(0.3)
        
        # PASSO 2: VERIFICANDO PYTHON
        self.atualizar_status("Verificando Python...", "🐍", 20)
        time.sleep(0.3)
        self.verificar_python()
        self.gui.refresh()
        time.sleep(0.3)
        
        # PASSO 3: VERIFICANDO VC++ REDISTRIBUTABLE
        self.atualizar_status("Verificando VC++ Redistributable...", "🖥️", 35)
        time.sleep(0.3)
        self.verificar_vc_redist()
        self.gui.refresh()
        time.sleep(0.3)
        
        # PASSO 4: VERIFICANDO PyQt6
        self.atualizar_status("Verificando PyQt6...", "📦", 50)
        time.sleep(0.3)
        self.verificar_pyqt()
        self.gui.refresh()
        time.sleep(0.3)
        
        # PASSO 5: VERIFICANDO FLASK
        self.atualizar_status("Verificando Flask...", "🌐", 65)
        time.sleep(0.3)
        self.verificar_flask()
        self.gui.refresh()
        time.sleep(0.3)
        
        # PASSO 6: VERIFICANDO PORTA
        self.atualizar_status("Verificando porta 5000...", "🔌", 80)
        time.sleep(0.3)
        self.verificar_porta()
        self.gui.refresh()
        time.sleep(0.3)
        
        # PASSO 7: VERIFICANDO PERMISSÕES
        self.atualizar_status("Verificando permissões...", "🔑", 90)
        time.sleep(0.3)
        self.verificar_permissoes()
        self.gui.refresh()
        time.sleep(0.3)
        
        # FINALIZA
        self.atualizar_status("✅ Diagnóstico concluído!", "✅", 100)
        self.log("✅ Diagnóstico concluído com sucesso!", "sucesso", "✅")
        time.sleep(0.5)
        self.mostrar_resultado()
        
    def verificar_assets(self):
        """Verifica pasta Assets e arquivos"""
        self.log("📁 Verificando Assets...", "info", "📁")
        
        if not os.path.exists("Assets"):
            self.log("❌ Pasta Assets NÃO encontrada!", "erro", "❌")
            self.problemas.append("Assets não encontrada")
            self.solucoes.append("Crie a pasta Assets")
            self.atualizar_status("❌ Assets não encontrada!", "❌")
            return
            
        self.log("✅ Pasta Assets encontrada!", "sucesso", "✅")
        self.atualizar_status("Assets encontrada, verificando arquivos...", "📁")
        
        arquivos = [
            ("Core/Base.py", "Biblioteca GUI"),
            ("Graphics/slider.svg", "Slider"),
            ("Graphics/checkbox.svg", "Checkbox"),
            ("Graphics/Label.svg", "Label"),
            ("Graphics/input-field.svg", "Input"),
            ("Graphics/progressbar.svg", "Progress"),
            ("Graphics/combobox.svg", "Combobox"),
            ("Graphics/web.svg", "Web"),
            ("Graphics/Pannel.svg", "Pannel"),
            ("Graphics/button.svg", "Button"),
            ("Graphic.css", "CSS"),
            ("Graphic.js", "JS"),
            ("CodeGenerator.js", "CodeGenerator"),
            ("PythonParser.js", "PythonParser"),
            ("DragDrop.js", "DragDrop"),
            ("Editor.js", "Editor"),
            ("Editor.css", "Editor CSS")
        ]
        
        total = len(arquivos)
        for i, (arquivo, descricao) in enumerate(arquivos):
            caminho = os.path.join("Assets", arquivo)
            progresso = 10 + int((i / total) * 10)
            self.atualizar_status(f"Verificando: {descricao}...", "📄", progresso)
            
            if os.path.exists(caminho):
                self.log(f"  ✅ {arquivo}", "sucesso", "✅")
            else:
                self.log(f"  ❌ {arquivo} FALTANDO!", "erro", "❌")
                self.problemas.append(f"Assets/{arquivo} faltando")
                self.solucoes.append(f"Copie {arquivo} para Assets/")
            
            time.sleep(0.03)
            
    def verificar_vc_redist(self):
        """Verifica se o VC++ Redistributable está instalado"""
        self.log("🖥️ Verificando VC++ Redistributable...", "info", "🖥️")
        self.atualizar_status("Verificando VC++ Redistributable...", "🖥️", 38)
        time.sleep(0.2)
        
        # Verifica no registro do Windows
        try:
            import winreg
            chave = r"SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64"
            chave2 = r"SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64"
            
            encontrado = False
            for key_path in [chave, chave2]:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                    winreg.CloseKey(key)
                    encontrado = True
                    break
                except:
                    pass
            
            if encontrado:
                self.log("  ✅ VC++ Redistributable instalado", "sucesso", "✅")
            else:
                self.log("  ⚠️ VC++ Redistributable NÃO encontrado", "alerta", "⚠️")
                self.problemas.append("VC++ Redistributable não instalado")
                self.solucoes.append("vc_redist.x64.exe")
                self.solucoes.append("Instale o Visual C++ Redistributable 2022")
        except:
            self.log("  ⚠️ Não foi possível verificar VC++ Redistributable", "alerta", "⚠️")
            
    def verificar_python(self):
        """Verifica Python"""
        self.log("🐍 Verificando Python...", "info", "🐍")
        self.atualizar_status("Verificando versão do Python...", "🐍", 25)
        time.sleep(0.2)
        
        versao = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.log(f"  ✅ Python {versao}", "sucesso", "✅")
        
        self.atualizar_status("Verificando arquitetura...", "🐍", 28)
        time.sleep(0.2)
        
        bits = 64 if sys.maxsize > 2**32 else 32
        if bits == 64:
            self.log(f"  ✅ Arquitetura: {bits}-bit", "sucesso", "✅")
        else:
            self.log(f"  ⚠️ Arquitetura: {bits}-bit (64-bit recomendado)", "alerta", "⚠️")
            self.problemas.append("Python 32-bit")
            self.solucoes.append("Instale Python 64-bit")
            
    def verificar_pyqt(self):
        """Verifica PyQt6 - COM DETECÇÃO DE ERRO DLL"""
        self.log("📦 Verificando PyQt6...", "info", "📦")
        self.atualizar_status("Verificando PyQt6...", "📦", 45)
        time.sleep(0.2)
        
        # Tenta importar de forma segura
        try:
            import PyQt6
            from PyQt6.QtCore import QT_VERSION
            self.log(f"  ✅ PyQt6 {QT_VERSION}", "sucesso", "✅")
            
            # Verifica WebEngine
            self.atualizar_status("Verificando WebEngine...", "🌐", 48)
            time.sleep(0.2)
            try:
                from PyQt6.QtWebEngineWidgets import QWebEngineView
                self.log("  ✅ WebEngine disponível", "sucesso", "✅")
            except ImportError:
                self.log("  ⚠️ WebEngine não disponível", "alerta", "⚠️")
                self.problemas.append("WebEngine não instalado")
                self.solucoes.append("pip install PyQt6-WebEngine")
                
        except ImportError as e:
            erro = str(e)
            if "DLL load failed" in erro:
                self.log("  ❌ ERRO DE DLL no PyQt6!", "erro", "❌")
                self.log(f"  📌 {erro[:100]}", "alerta", "💡")
                self.problemas.append("PyQt6 com erro de DLL")
                self.solucoes.append("vc_redist.x64.exe")
                self.solucoes.append("pip uninstall PyQt6 PyQt6-WebEngine -y && pip install PyQt6 PyQt6-WebEngine --force-reinstall --no-cache-dir")
                self.problemas.append("DLL do PyQt6 não carregou")
                self.solucoes.append("Instale o Visual C++ Redistributable 2022")
            else:
                self.log(f"  ❌ PyQt6 NÃO INSTALADO!", "erro", "❌")
                self.problemas.append("PyQt6 não instalado")
                self.solucoes.append("pip install PyQt6 PyQt6-WebEngine")
        except Exception as e:
            self.log(f"  ❌ Erro no PyQt6: {str(e)[:50]}", "erro", "❌")
            self.problemas.append("PyQt6 com problema")
            self.solucoes.append("Reinstale PyQt6: pip uninstall PyQt6 -y && pip install PyQt6")
            
    def verificar_flask(self):
        """Verifica Flask"""
        self.log("📦 Verificando Flask...", "info", "📦")
        self.atualizar_status("Verificando Flask...", "🌐", 65)
        time.sleep(0.2)
        
        try:
            import flask
            self.log(f"  ✅ Flask {flask.__version__}", "sucesso", "✅")
        except ImportError:
            self.log("  ❌ Flask NÃO INSTALADO!", "erro", "❌")
            self.problemas.append("Flask não instalado")
            self.solucoes.append("pip install flask flask-cors")
            
        self.atualizar_status("Verificando Flask-CORS...", "🌐", 68)
        time.sleep(0.2)
        
        try:
            import flask_cors
            self.log("  ✅ Flask-CORS", "sucesso", "✅")
        except ImportError:
            self.log("  ❌ Flask-CORS NÃO INSTALADO!", "erro", "❌")
            self.problemas.append("Flask-CORS não instalado")
            self.solucoes.append("pip install flask-cors")
            
    def verificar_porta(self):
        """Verifica porta 5000"""
        self.log("🔌 Verificando porta 5000...", "info", "🔌")
        self.atualizar_status("Verificando porta 5000...", "🔌", 82)
        time.sleep(0.2)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            resultado = sock.connect_ex(('127.0.0.1', 5000))
            sock.close()
            
            if resultado != 0:
                self.log("  ✅ Porta 5000 disponível", "sucesso", "✅")
            else:
                self.log("  ⚠️ Porta 5000 EM USO!", "alerta", "⚠️")
                self.problemas.append("Porta 5000 ocupada")
                self.solucoes.append("Feche programas na porta 5000")
        except:
            self.log("  ⚠️ Não foi possível verificar porta", "alerta", "⚠️")
            
    def verificar_permissoes(self):
        """Verifica permissões"""
        self.log("🔑 Verificando permissões...", "info", "🔑")
        self.atualizar_status("Verificando permissões...", "🔑", 92)
        time.sleep(0.2)
        
        try:
            test_file = "test_temp.tmp"
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            self.log("  ✅ Permissão de escrita OK", "sucesso", "✅")
        except:
            self.log("  ⚠️ Sem permissão para escrever", "alerta", "⚠️")
            self.problemas.append("Permissão negada")
            self.solucoes.append("Execute como Administrador")
            
    def mostrar_resultado(self):
        """Mostra resultado final com animação"""
        self.gui.set_widget_enabled(self.btn_abrir, True)
        
        if not self.problemas:
            self.gui.set_widget_text(
                self.resultado_label,
                "✅ TUDO OK! Sistema pronto para rodar."
            )
            self.gui.set_widget_enabled(self.btn_corrigir, False)
            self.gui.set_widget_text(self.btn_corrigir, "✅ OK")
            self.atualizar_status("✅ Sistema pronto!", "🎉", 100)
            self.log("🎉 Sistema 100% funcional!", "sucesso", "🎉")
        else:
            self.gui.set_widget_text(
                self.resultado_label,
                f"⚠️ {len(self.problemas)} problema(s) encontrado(s). Clique em Corrigir."
            )
            self.gui.set_widget_enabled(self.btn_corrigir, True)
            self.atualizar_status(f"⚠️ {len(self.problemas)} problema(s)", "⚠️", 100)
            self.log(f"⚠️ {len(self.problemas)} problema(s) detectado(s)", "alerta", "⚠️")
            
            # Lista os problemas no log
            for i, problema in enumerate(self.problemas, 1):
                self.log(f"  {i}. {problema}", "erro", "❌")
                
    def corrigir_problemas(self):
        """Corrige problemas automaticamente - INCLUINDO VC++ REDIST"""
        self.log("🔧 Iniciando correção...", "destaque", "🔧")
        self.atualizar_status("Corrigindo problemas...", "🔧", 0)
        self.gui.set_widget_enabled(self.btn_corrigir, False)
        
        correcoes = []
        baixar_vc = False
        
        for solucao in self.solucoes:
            if "pip install" in solucao:
                correcoes.append(solucao)
            elif "vc_redist.x64.exe" in solucao or "Visual C++ Redistributable" in solucao:
                baixar_vc = True
            elif "Crie a pasta Assets" in solucao:
                try:
                    os.makedirs("Assets", exist_ok=True)
                    self.log("✅ Pasta Assets criada!", "sucesso", "✅")
                    self.corrigidos.append("Assets criada")
                except:
                    self.log("❌ Erro ao criar Assets", "erro", "❌")
            elif "Copie o arquivo" in solucao:
                self.log(f"⚠️ Correção manual: {solucao}", "alerta", "⚠️")
        
        # ============================================
        # TENTA BAIXAR E INSTALAR VC++ REDISTRIBUTABLE
        # ============================================
        
        if baixar_vc:
            self.log("📥 Baixando Visual C++ Redistributable...", "info", "📥")
            self.atualizar_status("Baixando VC++ Redistributable...", "📥", 20)
            
            try:
                url_vc = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
                arquivo_vc = "vc_redist.x64.exe"
                
                self.log(f"  🌐 Baixando de: {url_vc}", "info", "🌐")
                
                # Baixa o arquivo
                urllib.request.urlretrieve(url_vc, arquivo_vc)
                self.log(f"  ✅ Download concluído: {arquivo_vc}", "sucesso", "✅")
                
                # Executa o instalador
                self.atualizar_status("Instalando VC++ Redistributable...", "🖥️", 40)
                self.log("  🖥️ Executando instalador...", "info", "🖥️")
                
                # Executa silenciosamente
                subprocess.run([arquivo_vc, "/install", "/quiet", "/norestart"], 
                              capture_output=True, check=False)
                
                self.log("  ✅ VC++ Redistributable instalado!", "sucesso", "✅")
                self.corrigidos.append("VC++ Redistributable instalado")
                
                # Remove o instalador
                try:
                    os.remove(arquivo_vc)
                except:
                    pass
                    
            except Exception as e:
                self.log(f"  ❌ Erro ao baixar/instalar VC++: {str(e)[:50]}", "erro", "❌")
                self.log("  💡 Baixe manualmente: https://aka.ms/vs/17/release/vc_redist.x64.exe", "alerta", "💡")
        
        # ============================================
        # INSTALA DEPENDÊNCIAS VIA PIP
        # ============================================
        
        if correcoes:
            self.log("📦 Instalando dependências...", "info", "📦")
            total = len(correcoes)
            
            for i, cmd in enumerate(correcoes):
                progresso = 50 + int((i / total) * 40)
                self.atualizar_status(f"Instalando: {cmd[:30]}...", "📦", progresso)
                self.log(f"▶️ {cmd}", "info", "📦")
                
                try:
                    # Tenta instalar com force-reinstall para corrigir DLLs
                    if "PyQt6" in cmd:
                        cmd_completo = "pip uninstall PyQt6 PyQt6-WebEngine -y && pip install PyQt6 PyQt6-WebEngine --force-reinstall --no-cache-dir"
                    else:
                        cmd_completo = cmd
                        
                    subprocess.run(cmd_completo.split(), capture_output=True, check=False)
                    self.log(f"✅ {cmd} executado", "sucesso", "✅")
                    self.corrigidos.append(cmd)
                except Exception as e:
                    self.log(f"❌ Erro: {cmd}", "erro", "❌")
                time.sleep(0.5)
        
        # ============================================
        # FINALIZA
        # ============================================
        
        if self.corrigidos:
            self.log(f"✅ {len(self.corrigidos)} correção(ões) aplicadas!", "sucesso", "✅")
            self.atualizar_status("✅ Correções aplicadas!", "✅", 100)
        else:
            self.log("⚠️ Nenhuma correção automática aplicada", "alerta", "⚠️")
            
        self.log("🔄 Re-diagnosticando...", "info", "🔄")
        self.gui.set_timer(2000, self.re_diagnosticar, repeat=False)
        
    def re_diagnosticar(self):
        """Re-diagnostica após correções"""
        self.problemas = []
        self.solucoes = []
        self.log("", "info")
        self.log("🔄 Novo diagnóstico...", "destaque", "🔄")
        self.gui.set_widget_text(self.log_text, "🔄 Reiniciando diagnóstico...\n")
        self.diagnosticar()
        
    def abrir_programa(self):
        """Abre o programa principal"""
        if self.problemas:
            self.log("⚠️ Corrija os problemas primeiro!", "alerta", "⚠️")
            return
            
        self.log("🚀 Iniciando programa...", "sucesso", "🚀")
        self.atualizar_status("Iniciando...", "🚀", 100)
        time.sleep(0.5)
        self.gui.close()
        
    def sair(self):
        """Sai do programa"""
        self.gui.close()
        
    def run(self):
        """Executa a interface"""
        self.criar_interface()
        self.gui.run()

# ============================================
# EXECUTA
# ============================================

if __name__ == "__main__":
    app = Diagnosticador()
    app.run()