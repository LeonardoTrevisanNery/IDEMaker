from BetterGuiSpark import GuiSpark
import subprocess
import sys
import os
import tkinter as tk
import ctypes
from ctypes import wintypes

# ========== FUNÇÕES PARA MULTIMONITOR ==========

def get_monitor_info(monitor_index=0):
    """Obtém informações de um monitor específico"""
    try:
        import ctypes
        from ctypes import wintypes
        
        user32 = ctypes.windll.user32
        
        # Estrutura para informações do monitor
        class MONITORINFOEX(ctypes.Structure):
            _fields_ = [
                ("cbSize", wintypes.DWORD),
                ("rcMonitor", wintypes.RECT),
                ("rcWork", wintypes.RECT),
                ("dwFlags", wintypes.DWORD),
                ("szDevice", ctypes.c_wchar * 32)
            ]
        
        # Callback para enumerar monitores
        monitors = []
        def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
            monitor_info = MONITORINFOEX()
            monitor_info.cbSize = ctypes.sizeof(MONITORINFOEX)
            if user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info)):
                monitors.append({
                    'handle': hMonitor,
                    'monitor': monitor_info.rcMonitor,
                    'work': monitor_info.rcWork,
                    'device': monitor_info.szDevice,
                    'is_primary': (monitor_info.dwFlags & 0x00000001) != 0  # MONITORINFOF_PRIMARY
                })
            return True
        
        # Enumerar todos os monitores
        monitor_enum = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(wintypes.RECT), ctypes.c_void_p)
        user32.EnumDisplayMonitors(None, None, monitor_enum(monitor_enum_proc), 0)
        
        if not monitors:
            return None
            
        # Selecionar o monitor pelo índice ou o primário
        if monitor_index < len(monitors):
            selected = monitors[monitor_index]
        else:
            # Se índice inválido, pega o primário
            selected = next((m for m in monitors if m['is_primary']), monitors[0])
        
        return {
            'monitor': selected['monitor'],
            'work': selected['work'],
            'device': selected['device'],
            'is_primary': selected['is_primary'],
            'x': selected['monitor'].left,
            'y': selected['monitor'].top,
            'width': selected['monitor'].right - selected['monitor'].left,
            'height': selected['monitor'].bottom - selected['monitor'].top,
            'work_x': selected['work'].left,
            'work_y': selected['work'].top,
            'work_width': selected['work'].right - selected['work'].left,
            'work_height': selected['work'].bottom - selected['work'].top
        }
    except:
        return None

def listar_monitores():
    """Lista todos os monitores disponíveis"""
    try:
        user32 = ctypes.windll.user32
        monitors = []
        
        class MONITORINFOEX(ctypes.Structure):
            _fields_ = [
                ("cbSize", wintypes.DWORD),
                ("rcMonitor", wintypes.RECT),
                ("rcWork", wintypes.RECT),
                ("dwFlags", wintypes.DWORD),
                ("szDevice", ctypes.c_wchar * 32)
            ]
        
        def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
            monitor_info = MONITORINFOEX()
            monitor_info.cbSize = ctypes.sizeof(MONITORINFOEX)
            if user32.GetMonitorInfoW(hMonitor, ctypes.byref(monitor_info)):
                rect = monitor_info.rcMonitor
                is_primary = (monitor_info.dwFlags & 0x00000001) != 0
                monitors.append({
                    'index': len(monitors),
                    'device': monitor_info.szDevice,
                    'x': rect.left,
                    'y': rect.top,
                    'width': rect.right - rect.left,
                    'height': rect.bottom - rect.top,
                    'is_primary': is_primary
                })
            return True
        
        monitor_enum = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(wintypes.RECT), ctypes.c_void_p)
        user32.EnumDisplayMonitors(None, None, monitor_enum(monitor_enum_proc), 0)
        
        return monitors
    except:
        return []

def obter_tamanho_workarea_global():
    """Obtém a área de trabalho de todos os monitores combinados"""
    try:
        user32 = ctypes.windll.user32
        rect = wintypes.RECT()
        user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0)  # SPI_GETWORKAREA
        return rect.right - rect.left, rect.bottom - rect.top
    except:
        return obter_tamanho_monitor()

def obter_tamanho_monitor_com_scale():
    """Obtém o tamanho do monitor considerando escala DPI (Windows)"""
    try:
        user32 = ctypes.windll.user32
        
        # Tenta obter escala DPI
        try:
            shcore = ctypes.windll.shcore
            shcore.SetProcessDPIAware()
            
            # Obtém DPI do monitor primário
            monitor = user32.MonitorFromWindow(0, 0x00000001)  # MONITOR_DEFAULTTOPRIMARY
            dpi_x = ctypes.c_uint()
            dpi_y = ctypes.c_uint()
            shcore.GetDpiForMonitor(monitor, 0, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
            
            scale = dpi_x.value / 96
        except:
            scale = 1.0
        
        # Obtém resolução física
        largura = user32.GetSystemMetrics(0)
        altura = user32.GetSystemMetrics(1)
        
        return int(largura / scale), int(altura / scale)
    except:
        return obter_tamanho_monitor()

# ========== FUNÇÕES ORIGINAIS (MODIFICADAS) ==========

def obter_tamanho_monitor():
    """Obtém a resolução do monitor principal"""
    try:
        root = tk.Tk()
        root.withdraw()
        largura = root.winfo_screenwidth()
        altura = root.winfo_screenheight()
        root.destroy()
        return largura, altura
    except:
        try:
            import ctypes
            user32 = ctypes.windll.user32
            largura = user32.GetSystemMetrics(0)
            altura = user32.GetSystemMetrics(1)
            return largura, altura
        except:
            try:
                import subprocess
                if sys.platform == "darwin":
                    return 1920, 1080
                else:
                    resultado = subprocess.run(
                        ['xrandr', '--current'],
                        capture_output=True, text=True
                    )
                    for linha in resultado.stdout.split('\n'):
                        if 'current' in linha and 'x' in linha:
                            partes = linha.split()
                            for parte in partes:
                                if 'x' in parte and 'current' in linha:
                                    res = parte.split('x')
                                    if len(res) == 2:
                                        return int(res[0]), int(res[1])
                    return 1920, 1080
            except:
                return 1920, 1080

def obter_tamanho_com_workarea():
    """Obtém a área de trabalho útil (excluindo taskbar)"""
    try:
        import ctypes
        user32 = ctypes.windll.user32
        rect = ctypes.wintypes.RECT()
        user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0)
        largura = rect.right - rect.left
        altura = rect.bottom - rect.top
        return largura, altura
    except:
        return obter_tamanho_monitor()

# ========== CONFIGURAÇÃO PRINCIPAL ==========

# Listar monitores disponíveis
print("=" * 50)
print("🔍 DETECTANDO MONITORES")
print("=" * 50)

monitores = listar_monitores()
if monitores:
    print(f"✅ {len(monitores)} monitor(es) detectado(s):")
    for i, mon in enumerate(monitores):
        primario = "⭐ PRIMÁRIO" if mon['is_primary'] else ""
        print(f"  Monitor {i}: {mon['width']}x{mon['height']} em ({mon['x']}, {mon['y']}) {primario}")
else:
    print("⚠️  Não foi possível listar monitores via API, usando fallback")

print("=" * 50)

# Seleciona o monitor (você pode mudar o índice)
MONITOR_SELECIONADO = 0  # 0 = primário, 1 = segundo, etc.

# Tenta obter informações do monitor selecionado
monitor_info = get_monitor_info(MONITOR_SELECIONADO)

if monitor_info:
    print(f"📺 Monitor {MONITOR_SELECIONADO} selecionado:")
    print(f"   Resolução total: {monitor_info['width']}x{monitor_info['height']}")
    print(f"   Posição: ({monitor_info['x']}, {monitor_info['y']})")
    print(f"   Área de trabalho: {monitor_info['work_width']}x{monitor_info['work_height']}")
    print(f"   Primário: {'Sim' if monitor_info['is_primary'] else 'Não'}")
    
    # Usar área de trabalho (exclui taskbar)
    largura = monitor_info['work_width']
    altura = monitor_info['work_height']
    
    # Posição do monitor (para janelas em monitores específicos)
    pos_x = monitor_info['work_x']
    pos_y = monitor_info['work_y']
else:
    # Fallback para métodos antigos
    print("⚠️  Usando método alternativo para detectar resolução")
    try:
        largura, altura = obter_tamanho_com_workarea()
        pos_x, pos_y = 0, 0
    except:
        largura, altura = obter_tamanho_monitor()
        pos_x, pos_y = 0, 0

# Ajustes para tela cheia
largura_janela = largura
altura_janela = altura

print(f"🖥️  Criando janela: {largura_janela}x{altura_janela}")
print(f"📍 Posição: ({pos_x}, {pos_y})")

# Cria a GUI com posição e tamanho
gui = GuiSpark("TestScreen", largura_janela, altura_janela )

# Se possível, define a posição da janela
try:
    gui.root.geometry(f"{largura_janela}x{altura_janela }+{pos_x}+{pos_y}")
except:
    pass

# ========== INICIA O COMPILLER.PY ==========

script_dir = os.path.dirname(os.path.abspath(__file__))
compiller_path = os.path.join(script_dir, "Compiller.py")

if sys.platform == "win32":
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    subprocess.Popen([pythonw, compiller_path], 
                     creationflags=subprocess.CREATE_NO_WINDOW,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
else:
    subprocess.Popen(["python3", compiller_path])

print("🚀 Compiller.py iniciado em background")

# ========== MOSTRA SPLASH ==========

gui.show_splash("Assets/Graphics/Splash.png", 600, 600, 5000)

# ========== ADICIONA WIDGET WEB ==========

gui.add_widget("web", 0, 0, largura_janela, altura_janela-20, url="http://localhost:5000")

print(f"🌐 Widget web adicionado: {largura_janela}x{altura_janela-20}")

# ========== EXECUTA A GUI ==========

try:
    gui.run()
    print("🔴 Janela fechada!")
except Exception as e:
    print(f"❌ Erro: {e}")
finally:
    try:
        os.kill(os.getpid(), 9)
    except:
        sys.exit(0)