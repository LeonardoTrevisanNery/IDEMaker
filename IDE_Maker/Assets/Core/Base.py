from PyQt6 import QtWidgets, QtCore, QtGui, sip
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import sys
import os
import csv
import json
import threading
import subprocess
import webbrowser
import os
import sys


class _KeyEventFilter(QtCore.QObject):
    def __init__(self, gui=None):
        super().__init__()
        self.gui = gui
        
    def eventFilter(self, watched, event):
        if event.type() in (QtCore.QEvent.Type.KeyPress, QtCore.QEvent.Type.KeyRelease):
            gui = self.gui
            if not hasattr(gui, '_key_event_handlers'):
                return super().eventFilter(watched, event)

            widget_id = id(watched)
            handlers = gui._key_event_handlers.get(widget_id, [])
            if not handlers:
                return super().eventFilter(watched, event)

            for handler in handlers:
                if event.type() == QtCore.QEvent.Type.KeyPress and handler['state'] != 'pressed':
                    continue
                if event.type() == QtCore.QEvent.Type.KeyRelease and handler['state'] != 'released':
                    continue

                key = handler['key']
                qt_key = handler['qt_key']
                str_key = handler['str_key']
                command = handler['command']

                try:
                    if key is None:
                        command()
                    elif str_key and event.text().lower() == str_key:
                        command()
                    elif qt_key and event.key() == qt_key:
                        command()
                except Exception:
                    pass

        return super().eventFilter(watched, event)


class _MouseEventFilter(QtCore.QObject):
    def __init__(self, gui=None):
        super().__init__()
        self.gui = gui

    def eventFilter(self, watched, event):
        if event.type() in (
            QtCore.QEvent.Type.MouseButtonPress,
            QtCore.QEvent.Type.MouseButtonDblClick,
            QtCore.QEvent.Type.Enter,
            QtCore.QEvent.Type.Leave
        ):
            gui = self.gui
            if not hasattr(gui, '_mouse_event_handlers'):
                return super().eventFilter(watched, event)

            widget_id = id(watched)
            handlers = gui._mouse_event_handlers.get(widget_id, []) + gui._mouse_event_handlers.get(None, [])
            if not handlers:
                return super().eventFilter(watched, event)

            event_type = None
            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                event_type = 'click'
            elif event.type() == QtCore.QEvent.Type.MouseButtonDblClick:
                event_type = 'double_click'
            elif event.type() == QtCore.QEvent.Type.Enter:
                event_type = 'enter'
            elif event.type() == QtCore.QEvent.Type.Leave:
                event_type = 'leave'

            for handler in handlers:
                if handler['event_type'] != event_type:
                    continue

                widget = watched
                command = handler['command']
                if event_type in ('click', 'double_click'):
                    pos = event.position()
                    print(f"Clicado em {widget.__class__.__name__} em ({pos.x():.0f}, {pos.y():.0f})")

                try:
                    command(widget, event)
                except TypeError:
                    try:
                        command(event)
                    except TypeError:
                        command()
                except Exception:
                    pass

        return super().eventFilter(watched, event)


class GuiSpark:
    def __init__(self, title="PyQt GUI Manager", width=600, height=400):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle(title)
        self.window.resize(width, height)

        self.central = QtWidgets.QWidget()
        self.window.setCentralWidget(self.central)
        
        # Layout principal para melhor organização
        self.main_layout = QtWidgets.QVBoxLayout(self.central)
        
        self.widgets = {}
        self.current_focus = None
        self.current_theme = None
        self._timers = []
        self._threads = []
        self._key_event_handlers = {}
        self._key_event_filter = _KeyEventFilter(self)
        self._mouse_event_handlers = {}
        self._mouse_event_filter = _MouseEventFilter(self)
        self.app.installEventFilter(self._mouse_event_filter)
    def set_timer(self, ms, command, repeat=False):
     """
     Cria um timer.
 
     Exemplo:
 
     gui.set_timer(1000, atualizar)
 
     gui.set_timer(
         100,
         atualizar,
         repeat=True
     )
     """
 
     timer = QtCore.QTimer()
 
     timer.timeout.connect(command)
 
     if repeat:
 
         timer.start(ms)
 
     else:
 
         timer.setSingleShot(True)
 
         timer.timeout.connect(timer.deleteLater)
 
         timer.start(ms)
 
     self._timers.append(timer)
 
     return timer
    
    def stop_timer(self, timer):

     if timer:

        timer.stop()

        if timer in self._timers:

            self._timers.remove(timer)
    
    def stop_all_timers(self):

     for timer in self._timers:

        timer.stop()

     self._timers.clear()

    def run_thread(self, command, daemon=True):

     thread = threading.Thread(
         target=command,
         daemon=daemon
     )
 
     thread.start()
 
     self._threads.append(thread)
 
     return thread

    def wait_thread(self, thread):
     if thread:

        thread.join()
    

    def get_clipboard(self):

     return self.app.clipboard().text()

    def set_clipboard(self, text):

     self.app.clipboard().setText(str(text))

    def clear_clipboard(self):

     self.app.clipboard().clear()

    def open_program(self, program, *args):
    
        return subprocess.Popen(
            [program, *args]
        )
    def open_folder(self, path):

     os.startfile(path)
    
    def open_url(self, url):

     webbrowser.open(url)

    def open_file(self, path):

     os.startfile(path)

    def execute(self, command):
    
        return subprocess.Popen(
            command,
            shell=True
        )
    def restart(self):
    
        python = sys.executable
    
        os.execl(
            python,
            python,
            *sys.argv
        )

    def close(self):

     self.app.quit()
    

    def refresh(self):

     QtWidgets.QApplication.processEvents()
    
    def sleep(self, seconds):

     self.wait(
 
         int(seconds * 1000)
 
     )
    def screenshot(self, filename="screenshot.png"):

     pixmap = self.window.grab()

     pixmap.save(filename)

     return filename
    
    def add_shortcut(self, shortcut, command):

     shortcut = QtGui.QShortcut(
        QtGui.QKeySequence(shortcut),
        self.window
     )

     shortcut.activated.connect(command)

     return shortcut
    
    def enable_drag_drop(self, command):

     self.window.setAcceptDrops(True)

     def dragEnterEvent(event):

        event.acceptProposedAction()

     def dropEvent(event):

        arquivos = []

        for url in event.mimeData().urls():

            arquivos.append(url.toLocalFile())

        command(arquivos)

     self.window.dragEnterEvent = dragEnterEvent

     self.window.dropEvent = dropEvent
    def create_table(self,x,y,w,h,rows,cols):

     table = QtWidgets.QTableWidget(rows,cols,self.central)
 
     table.setGeometry(x,y,w,h)
 
     table.show()
 
     return table
    def pick_font(self):

     return QtWidgets.QFontDialog.getFont()[0]
    def toast(self,text):

     self.status.showMessage(text,3000)

    def create_tray(self,icon):

      tray = QtWidgets.QSystemTrayIcon(
  
          QtGui.QIcon(icon),
  
          self.window
  
      )
  
      tray.show()
  
      return tray
    def show_splash(self, image, width, height, ms=3000):

     pix = QtGui.QPixmap(image)

     pix = pix.scaled(
        width,
        height,
        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
        QtCore.Qt.TransformationMode.SmoothTransformation
     )

     splash = QtWidgets.QSplashScreen(pix)

     splash.show()

     QtWidgets.QApplication.processEvents()

     self.wait(ms)

     splash.close()
    
    def fade_in(self,widget,duration=500):

     effect = QtWidgets.QGraphicsOpacityEffect(widget)
 
     widget.setGraphicsEffect(effect)
 
     anim = QtCore.QPropertyAnimation(effect,b"opacity")
 
     anim.setDuration(duration)
 
     anim.setStartValue(0)
 
     anim.setEndValue(1)
 
     anim.start()
 
     return anim
    def move_animation(self,widget,x,y,duration=500):

     anim = QtCore.QPropertyAnimation(widget,b"geometry")
 
     anim.setDuration(duration)
 
     g = widget.geometry()
 
     anim.setStartValue(g)
 
     anim.setEndValue(QtCore.QRect(x,y,g.width(),g.height()))
 
     anim.start()
 
     return anim
    def set_font_size(self, wid, size):
     """
     Define o tamanho da fonte de um widget.
 
     Exemplo:
         gui.set_font_size(label, 20)
         gui.set_font_size(botao, 14)
     """
 
     if wid not in self.widgets:
         return
 
     widget = self.widgets[wid]["widget"]
 
     font = widget.font()
     font.setPointSize(size)
     widget.setFont(font)

    def show_console(self):

     import ctypes

     ctypes.windll.user32.ShowWindow(

        ctypes.windll.kernel32.GetConsoleWindow(),

        5

    )


    def _build_stylesheet(self, wtype, bg=None, fg=None, hover_bg=None, pressed_bg=None, border_radius=None):
        """Constrói a folha de estilo de forma mais robusta"""
        styles = []
        
        base_props = []
        if bg:
            base_props.append(f"background-color: {bg}")
        if fg:
            base_props.append(f"color: {fg}")
        if border_radius:
            base_props.append(f"border-radius: {border_radius}px")
        
        if base_props:
            if wtype == 'button':
                styles.append(f"QPushButton {{ {'; '.join(base_props)} }}")
            elif wtype == 'label':
                styles.append(f"QLabel {{ {'; '.join(base_props)} }}")
            elif wtype == 'frame':
                styles.append(f"QFrame {{ {'; '.join(base_props)} }}")
            elif wtype == 'entry':
                styles.append(f"QLineEdit {{ {'; '.join(base_props)} }}")
            elif wtype == 'text':
                styles.append(f"QTextEdit {{ {'; '.join(base_props)} }}")
            elif wtype == 'checkbox':
                styles.append(f"QCheckBox {{ {'; '.join(base_props)} }}")
            elif wtype == 'web':
                styles.append(f"QWebEngineView {{ {'; '.join(base_props)} }}")
            elif wtype == 'slider':
                styles.append(f"QSlider {{ {'; '.join(base_props)} }}")
            elif wtype == 'progress':
                styles.append(f"QProgressBar {{ {'; '.join(base_props)} }}")
            elif wtype == 'combobox':
                styles.append(f"QComboBox {{ {'; '.join(base_props)} }}")
            else:
                styles.append(f"{'; '.join(base_props)}")
        
        if wtype == 'button':
            if hover_bg:
                styles.append(f"QPushButton:hover {{ background-color: {hover_bg} }}")
            if pressed_bg:
                styles.append(f"QPushButton:pressed {{ background-color: {pressed_bg} }}")
        
        return "".join(styles)

    def add_widget(self, wtype, x=0, y=0, width=100, height=30, text="", bg=None, fg=None,
                   hover_bg=None, pressed_bg=None, border_radius=None, command=None, parent=None,
                   placeholder="", url=None, min_value=0, max_value=100, value=0, 
                   items=None, orientation='horizontal'):
        """
        Adiciona um widget
        
        Args:
            wtype: button, label, frame, entry, text, checkbox, web, slider, progress, combobox
            min_value/max_value: Para sliders e progress bars
            value: Valor inicial
            items: Lista de itens para combobox
            orientation: 'horizontal' ou 'vertical' para slider
        """
        parent = parent or self.central

        if wtype == 'button':
            widget = QtWidgets.QPushButton(text, parent)
        elif wtype == 'label':
            widget = QtWidgets.QLabel(text, parent)
        elif wtype == 'frame':
            widget = QtWidgets.QFrame(parent)
            widget.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        elif wtype == 'entry':
            widget = QtWidgets.QLineEdit(parent)
            if text:
                widget.setText(text)
            if placeholder:
                widget.setPlaceholderText(placeholder)
        elif wtype == 'text':
            widget = QtWidgets.QTextEdit(parent)
            if text:
                widget.setText(text)
            if placeholder:
                widget.setPlaceholderText(placeholder)
        elif wtype == 'checkbox':
            widget = QtWidgets.QCheckBox(text, parent)
            widget.setChecked(bool(value))
        elif wtype == 'web':
            widget = QWebEngineView(parent)
            if url:
                if url.startswith(('http://', 'https://')):
                    widget.load(QUrl(url))
                else:
                    widget.setHtml(url)
            elif text:
                widget.setHtml(text)
        elif wtype == 'slider':  # NOVO: Slider
            widget = QtWidgets.QSlider(parent)
            if orientation == 'horizontal':
                widget.setOrientation(QtCore.Qt.Orientation.Horizontal)
            else:
                widget.setOrientation(QtCore.Qt.Orientation.Vertical)
            widget.setMinimum(min_value)
            widget.setMaximum(max_value)
            widget.setValue(value)
        elif wtype == 'progress':  # NOVO: Progress Bar
            widget = QtWidgets.QProgressBar(parent)
            widget.setMinimum(min_value)
            widget.setMaximum(max_value)
            widget.setValue(value)
        elif wtype == 'combobox':  # NOVO: Combobox
            widget = QtWidgets.QComboBox(parent)
            if items:
                widget.addItems(items)
            if text:
                widget.setCurrentText(text)
        else:
            raise ValueError(f"Tipo de widget desconhecido: {wtype}")

        stylesheet = self._build_stylesheet(wtype, bg, fg, hover_bg, pressed_bg, border_radius)
        if stylesheet:
            widget.setStyleSheet(stylesheet)

        widget.setGeometry(x, y, width, height)

        if command and wtype in ['button', 'checkbox', 'slider', 'combobox']:
            if wtype == 'button':
                widget.clicked.connect(command)
            elif wtype == 'checkbox':
                widget.stateChanged.connect(command)
            elif wtype == 'slider':
                widget.valueChanged.connect(command)
            elif wtype == 'combobox':
                widget.currentTextChanged.connect(command)

        wid = id(widget)
        self.widgets[wid] = {'widget': widget, 'type': wtype}
        widget.show()
        return wid

    def remove_widget(self, wid):
        """Remove um widget pelo ID"""
        if wid in self.widgets:
            widget = self.widgets[wid]['widget']
            if widget.parent() and hasattr(widget.parent(), 'layout') and widget.parent().layout():
                widget.parent().layout().removeWidget(widget)
            widget.setParent(None)
            widget.deleteLater()
            del self.widgets[wid]

    def add_layout_widget(self, wtype, x=0, y=0, width=100, height=30, text="", bg=None, fg=None, command=None, placeholder="", 
                         url=None, min_value=0, max_value=100, value=0, items=None, orientation='horizontal', parent=None):
        """Adiciona widget com posicionamento direto.

        Argumentos `x` e `y` são independentes e, se não fornecidos, assumem 0.
        """
        parent = parent or self.central

        if wtype == 'button':
            widget = QtWidgets.QPushButton(text, parent)
        elif wtype == 'label':
            widget = QtWidgets.QLabel(text, parent)
        elif wtype == 'entry':
            widget = QtWidgets.QLineEdit(parent)
            if placeholder:
                widget.setPlaceholderText(placeholder)
        elif wtype == 'checkbox':
            widget = QtWidgets.QCheckBox(text, parent)
            widget.setChecked(bool(value))
        elif wtype == 'web':
            widget = QWebEngineView(parent)
            if url:
                if url.startswith(('http://', 'https://')):
                    widget.load(QUrl(url))
                else:
                    widget.setHtml(url)
            elif text:
                widget.setHtml(text)
        elif wtype == 'slider':  # NOVO: Slider no layout
            widget = QtWidgets.QSlider(parent)
            if orientation == 'horizontal':
                widget.setOrientation(QtCore.Qt.Orientation.Horizontal)
            else:
                widget.setOrientation(QtCore.Qt.Orientation.Vertical)
            widget.setMinimum(min_value)
            widget.setMaximum(max_value)
            widget.setValue(value)
        elif wtype == 'progress':  # NOVO: Progress Bar no layout
            widget = QtWidgets.QProgressBar(parent)
            widget.setMinimum(min_value)
            widget.setMaximum(max_value)
            widget.setValue(value)
        elif wtype == 'combobox':  # NOVO: Combobox no layout
            widget = QtWidgets.QComboBox(parent)
            if items:
                widget.addItems(items)
            if text:
                widget.setCurrentText(text)
        else:
            raise ValueError(f"Tipo não suportado para layout: {wtype}")
        
        stylesheet = self._build_stylesheet(wtype, bg, fg)
        if stylesheet:
            widget.setStyleSheet(stylesheet)
        
        if command and wtype in ['button', 'checkbox', 'slider', 'combobox']:
            if wtype == 'button':
                widget.clicked.connect(command)
            elif wtype == 'checkbox':
                widget.stateChanged.connect(command)
            elif wtype == 'slider':
                widget.valueChanged.connect(command)
            elif wtype == 'combobox':
                widget.currentTextChanged.connect(command)

        widget.setGeometry(x, y, width, height)
        widget.show()

        wid = id(widget)
        self.widgets[wid] = {'widget': widget, 'type': wtype}
        return wid

    def get_widget_text(self, wid):
        """Obtém texto/valor de um widget"""
        if wid in self.widgets:
            widget = self.widgets[wid]['widget']
            wtype = self.widgets[wid]['type']
            
            if wtype in ['entry']:
                return widget.text()
            elif wtype in ['text']:
                return widget.toPlainText()
            elif wtype in ['label', 'button']:
                return widget.text()
            elif wtype == 'checkbox':
                return widget.isChecked()
            elif wtype == 'web':
                return widget.url().toString()
            elif wtype == 'slider':  # NOVO: Valor do slider
                return widget.value()
            elif wtype == 'progress':  # NOVO: Valor do progress
                return widget.value()
            elif wtype == 'combobox':  # NOVO: Texto selecionado no combobox
                return widget.currentText()
        return None

    def set_widget_text(self, wid, text):
        """Define texto/valor de um widget"""
        if wid in self.widgets:
            widget = self.widgets[wid]['widget']
            wtype = self.widgets[wid]['type']
            if wtype in ['entry']:
                widget.setText(str(text))
            elif wtype in ['text']:
                widget.setPlainText(str(text))
            elif wtype in ['label', 'button']:
                widget.setText(str(text))
            elif wtype == 'checkbox':
                widget.setChecked(bool(text))
            elif wtype == 'web':
                if str(text).startswith(('http://', 'https://')):
                    widget.load(QUrl(str(text)))
                else:
                    widget.setHtml(str(text))
            elif wtype == 'slider':  # NOVO: Setar valor do slider
                try:
                    widget.setValue(int(text))
                except (ValueError, TypeError):
                    pass
           
            elif wtype == 'progress':  # NOVO: Setar valor do progress
                try:
                    widget.setValue(int(text))
                except (ValueError, TypeError):
                    pass
            elif wtype == 'combobox':  # NOVO: Setar texto no combobox
                widget.setCurrentText(str(text))

    def set_widget_visibility(self, wid, visible):
        """Mostra/oculta widget"""
        if wid in self.widgets:
            widget = self.widgets[wid]['widget']
            widget.setVisible(visible)

    def set_widget_enabled(self, wid, enabled):
        """Habilita/desabilita widget"""
        if wid in self.widgets:
            widget = self.widgets[wid]['widget']
            widget.setEnabled(enabled)

    def clear_container(self, parent_wid=None):
        """Limpa todos widgets de um container"""
        parent = self.central if not parent_wid else self.widgets[parent_wid]['widget']
        for child in parent.findChildren(QtWidgets.QWidget):
            if child != parent:
                child_id = id(child)
                if child_id in self.widgets:
                    self.remove_widget(child_id)

    def show_message(self, title, message, message_type="info", bg=None, fg=None, text=None, button_bg=None, button_fg=None, buttonfg=None):
        """Exibe caixa de mensagem com cores customizáveis"""
        box = QtWidgets.QMessageBox(self.window)
        box.setWindowTitle(title)
        box.setText(message)

        if message_type == "info":
            box.setIcon(QtWidgets.QMessageBox.Icon.Information)
        elif message_type == "warning":
            box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        elif message_type == "error":
            box.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        else:
            box.setIcon(QtWidgets.QMessageBox.Icon.NoIcon)

        effective_fg = text if text is not None else fg
        button_foreground = button_fg if button_fg is not None else buttonfg
        if bg or effective_fg or button_bg or button_foreground:
            stylesheet = []
            if bg:
                stylesheet.append(f"QMessageBox {{ background-color: {bg}; }}")
            if effective_fg:
                stylesheet.append(f"QMessageBox QLabel {{ color: {effective_fg}; }}")
            button_styles = []
            if button_bg:
                button_styles.append(f"background-color: {button_bg};")
            if button_foreground:
                button_styles.append(f"color: {button_foreground};")
            button_styles.append("min-width: 80px;")
            stylesheet.append(f"QMessageBox QPushButton {{ {' '.join(button_styles)} }}")
            box.setStyleSheet("\n".join(stylesheet))

        box.exec()

    # ========== SISTEMA DE TEMAS ==========

    def set_theme(self, theme_name="light", theme=None, **custom_theme):
        """Aplica um tema pré-definido ou customizado à interface.

        Args:
            theme_name: Nome do tema ('light', 'dark', 'blue', 'green', 'custom') ou
                um dicionário de tema customizado.
            theme: Dicionário com as chaves 'bg', 'fg', 'widget_bg', 'widget_fg' e 'accent'.
            custom_theme: Valores individuais para bg, fg, widgetbg/widget_bg,
                widgetfg/widget_fg e accent.
        """
        themes = {
            "dark": {
                "bg": "#2b2b2b",
                "fg": "#ffffff",
                "widget_bg": "#3c3f41",
                "widget_fg": "#ffffff",
                "accent": "#af72fa"
            },
            "light": {
                "bg": "#f5f5f5",
                "fg": "#333333",
                "widget_bg": "#ffffff",
                "widget_fg": "#333333",
                "accent": "#2196F3"
            },
            "blue": {
                "bg": "#e3f2fd",
                "fg": "#1565c0",
                "widget_bg": "#bbdefb",
                "widget_fg": "#0d47a1",
                "accent": "#1976d2"
            },
            "green": {
                "bg": "#e8f5e8",
                "fg": "#2e7d32",
                "widget_bg": "#c8e6c9",
                "widget_fg": "#1b5e20",
                "accent": "#4caf50"
            },
            "custom": {
                "bg": "#ffffff",
                "fg": "#000000",
                "widget_bg": "#f0f0f0",
                "widget_fg": "#000000",
                "accent": "#ff5722"
            }
        }

        user_values = {}
        if isinstance(theme_name, dict):
            user_values.update(theme_name)
            theme_name = "custom"
            theme = None
        elif isinstance(theme, dict):
            user_values.update(theme)

        user_values.update(custom_theme)

        if theme_name == "custom":
            theme = themes["custom"].copy()
            normalized = {}
            for key, value in user_values.items():
                if value is None:
                    continue
                normalized_key = {
                    "widgetbg": "widget_bg",
                    "widgetfg": "widget_fg"
                }.get(key, key)
                normalized[normalized_key] = value

            theme.update(normalized)
        else:
            theme = themes.get(theme_name, themes["light"])

        stylesheet = f"""
            QWidget {{
                background-color: {theme['bg']};
                color: {theme['fg']};
            }}
            QPushButton {{
                background-color: {theme['widget_bg']};
                color: {theme['widget_fg']};
                border: 1px solid {theme['accent']};
                padding: 5px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: {theme['accent']};
            }}
            QLineEdit, QTextEdit, QComboBox {{
                background-color: {theme['widget_bg']};
                color: {theme['widget_fg']};
                border: 1px solid {theme['accent']};
                border-radius: 3px;
                padding: 2px;
            }}
            QSlider::groove:horizontal {{
                border: 1px solid {theme['accent']};
                height: 8px;
                background: {theme['widget_bg']};
                margin: 2px 0;
                border-radius: 4px;
            }}
            QSlider::handle:horizontal {{
                background: {theme['accent']};
                border: 1px solid {theme['accent']};
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }}
            QProgressBar {{
                border: 1px solid {theme['accent']};
                border-radius: 4px;
                text-align: center;
                background: {theme['widget_bg']};
            }}
            QProgressBar::chunk {{
                background-color: {theme['accent']};
                border-radius: 3px;
            }}
        """
        self.central.setStyleSheet(stylesheet)
        self.window.setStyleSheet(stylesheet)
        self.app.setStyleSheet(stylesheet)
        self.current_theme = theme
        self.window.repaint()
        QtWidgets.QApplication.processEvents()

    # ========== VALIDAÇÃO DE ENTRADA ==========

    def set_input_validation(self, wid, validation_type="text", max_length=None, regex=None):
        """
        Configura validação para campos de entrada
        
        Args:
            wid: ID do widget
            validation_type: 'text', 'number', 'email', 'custom'
            max_length: Comprimento máximo
            regex: Expressão regular personalizada
        """
        if wid not in self.widgets:
            return
        
        widget = self.widgets[wid]['widget']
        wtype = self.widgets[wid]['type']
        
        if wtype not in ['entry', 'text']:
            return
        
        if max_length:
            widget.setMaxLength(max_length)
        
        if validation_type == "number":
            from PyQt6.QtGui import QDoubleValidator
            validator = QDoubleValidator()
            widget.setValidator(validator)
        elif validation_type == "integer":
            from PyQt6.QtGui import QIntValidator
            validator = QIntValidator()
            widget.setValidator(validator)
        elif validation_type == "email":
            import re
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            from PyQt6.QtGui import QRegularExpressionValidator
            from PyQt6.QtCore import QRegularExpression
            regex = QRegularExpression(email_regex)
            validator = QRegularExpressionValidator(regex)
            widget.setValidator(validator)
        elif validation_type == "custom" and regex:
            from PyQt6.QtGui import QRegularExpressionValidator
            from PyQt6.QtCore import QRegularExpression
            regex_obj = QRegularExpression(regex)
            validator = QRegularExpressionValidator(regex_obj)
            widget.setValidator(validator)

    # ========== EVENTOS AVANÇADOS ==========

    def add_mouse_event(self, wid=None, event_type="click", command=None):
        """
        Adiciona eventos de mouse a widgets.

        Se `wid` não for fornecido, o evento será aplicado a qualquer widget clicado.
        A função `command` pode aceitar:
            - command(widget, event)
            - command(event)
            - command()
        """
        if not command:
            return

        if event_type not in ('click', 'double_click', 'enter', 'leave'):
            return

        if wid is not None and wid not in self.widgets:
            return

        widget_id = None
        if wid is not None:
            widget = self.widgets[wid]['widget']
            widget_id = id(widget)
            widget.setMouseTracking(True)
        else:
            widget = None

        self._mouse_event_handlers.setdefault(widget_id, []).append({
            'event_type': event_type,
            'command': command
        })

        return True
        
        if event_type == "click":
            # CORREÇÃO: Preservar o evento original
            original_event = widget.mousePressEvent
            def new_event(event):
                command()
                if original_event:
                    original_event(event)
            widget.mousePressEvent = new_event
            
        elif event_type == "double_click":
            original_event = widget.mouseDoubleClickEvent
            def new_event(event):
                command()
                if original_event:
                    original_event(event)
            widget.mouseDoubleClickEvent = new_event
            
        elif event_type == "enter":
            original_event = widget.enterEvent
            def new_event(event):
                command()
                if original_event:
                    original_event(event)
            widget.enterEvent = new_event
            
        elif event_type == "leave":
            original_event = widget.leaveEvent
            def new_event(event):
                command()
                if original_event:
                    original_event(event)
            widget.leaveEvent = new_event

    def add_key_event(self, wid=None, key=None, state="pressed", command=None):
        """Adiciona evento de tecla a um widget.

        Se `wid` não for fornecido, o evento será aplicado ao widget que atualmente tem foco.
        """
        if not command:
            return

        if wid is None:
            widget = QtWidgets.QApplication.focusWidget() or self.central
            if widget is None:
                return
        else:
            if wid not in self.widgets:
                return
            widget = self.widgets[wid]['widget']

        widget.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        widget.setFocus()
        widget.installEventFilter(self._key_event_filter)

        qt_key = None
        str_key = None

        if isinstance(key, str):
            str_key = key.lower().strip()
            aliases = {
                "esc": "Escape",
                "escape": "Escape",
                "enter": "Return",
                "return": "Return",
                "space": "Space",
                "capslock": "CapsLock",
                "del": "Delete",
                "delete": "Delete",
                "pgup": "PageUp",
                "pageup": "PageUp",
                "pgdown": "PageDown",
                "pagedown": "PageDown",
                "ins": "Insert",
                "insert": "Insert",
                "backspace": "Backspace",
                "tab": "Tab",
                "up": "Up",
                "down": "Down",
                "left": "Left",
                "right": "Right",
                "home": "Home",
                "end": "End",
                "shift": "Shift",
                "ctrl": "Control",
                "control": "Control",
                "alt": "Alt",
                "meta": "Meta",
                "super": "Meta",
            }

            name = aliases.get(str_key, str_key.upper())
            qt_key = getattr(QtCore.Qt, f"Key_{name}", None)
        elif isinstance(key, int):
            qt_key = key

        if state not in ("pressed", "released"):
            return

        handler_config = {
            'key': key,
            'qt_key': qt_key,
            'str_key': str_key,
            'state': state,
            'command': command
        }
        widget_id = id(widget)
        self._key_event_handlers.setdefault(widget_id, []).append(handler_config)

    # ========== FUNÇÕES PARA MANIPULAÇÃO DE ARQUIVO ==========

    def save_to_file(self, data, filename=None, file_type=None, mode="w", separator=","):
        """
        Salva dados em arquivo com extensão escolhida pelo usuário
        """
        if filename is None:
            filename, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
                self.window, 
                "Salvar Arquivo", 
                "", 
                "Todos os arquivos (*);;Text files (*.txt);;CSV files (*.csv);;JSON files (*.json)"
            )
            if not filename:
                return False
            
            if selected_filter:
                if "txt" in selected_filter:
                    file_type = "txt"
                elif "csv" in selected_filter:
                    file_type = "csv"
                elif "json" in selected_filter:
                    file_type = "json"
        
        if file_type is None and filename:
            ext = os.path.splitext(filename)[1].lower().replace('.', '')
            if ext in ['txt', 'csv', 'json']:
                file_type = ext
            else:
                file_type = 'txt'
        
        try:
            with open(filename, mode, encoding='utf-8') as file:
                if file_type == 'txt':
                    if isinstance(data, list):
                        if any('\n' in str(item) for item in data) or any(separator in str(item) for item in data):
                            file.write('\n'.join(str(item) for item in data))
                        else:
                            file.write(separator.join(str(item) for item in data))
                    else:
                        file.write(str(data))
                
                elif file_type == 'csv':
                    if isinstance(data, list):
                        if all(isinstance(item, (list, tuple)) for item in data):
                            writer = csv.writer(file)
                            writer.writerows(data)
                        else:
                            writer = csv.writer(file)
                            writer.writerow(data)
                    else:
                        file.write(str(data))
                
                elif file_type == 'json':
                    if isinstance(data, (dict, list)):
                        json.dump(data, file, indent=4, ensure_ascii=False)
                    else:
                        file.write(str(data))
                
                else:
                    file.write(str(data))
            
            self.show_message("Sucesso", f"Arquivo salvo: {filename}", "info")
            return True
            
        except Exception as e:
            self.show_message("Erro", f"Erro ao salvar arquivo: {str(e)}", "error")
            return False

    def read_from_file(self, filename=None, file_type=None):
        """
        Lê dados de um arquivo e retorna o conteúdo
        """
        if filename is None:
            filename, selected_filter = QtWidgets.QFileDialog.getOpenFileName(
                self.window,
                "Abrir Arquivo",
                "",
                "Todos os arquivos (*);;Text files (*.txt);;CSV files (*.csv);;JSON files (*.json)"
            )
            if not filename:
                return None
            
            if selected_filter:
                if "txt" in selected_filter:
                    file_type = "txt"
                elif "csv" in selected_filter:
                    file_type = "csv"
                elif "json" in selected_filter:
                    file_type = "json"
        
        if file_type is None and filename:
            ext = os.path.splitext(filename)[1].lower().replace('.', '')
            if ext in ['txt', 'csv', 'json']:
                file_type = ext
            else:
                file_type = 'txt'
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                if file_type == 'txt':
                    content = file.read()
                    if ',' in content and '\n' not in content:
                        return [item.strip() for item in content.split(',')]
                    elif '\n' in content:
                        return [line.strip() for line in content.split('\n') if line.strip()]
                    else:
                        return content
                
                elif file_type == 'csv':
                    reader = csv.reader(file)
                    rows = list(reader)
                    if len(rows) == 1:
                        return rows[0]
                    else:
                        return rows
                
                elif file_type == 'json':
                    return json.load(file)
                
                else:
                    return file.read()
                    
        except Exception as e:
            self.show_message("Erro", f"Erro ao ler arquivo: {str(e)}", "error")
            return None

    def append_to_file(self, data, filename=None, file_type=None, separator=","):
        """
        Adiciona dados a um arquivo existente
        """
        return self.save_to_file(data, filename, file_type, mode="a", separator=separator)

    def run(self):
        self.window.show()
        return self.app.exec()
    def wait(self, ms):
     loop = QtCore.QEventLoop()
     QtCore.QTimer.singleShot(ms, loop.quit)
     loop.exec()