// ============================================
// EDITOR DE CÓDIGO
// ============================================

let modoAtual = 'visual';
let codigoOriginal = '';

function Visual() {
    const designer = document.getElementById("modoVisual");
    const editor = document.getElementById("modoTexto");
    const codeEditor = document.getElementById("codigoEditor");
    
    designer.style.display = "none";
    editor.style.display = "flex";
    codeEditor.style.display = "block";
    modoAtual = 'texto';
    
    if (window.codeLock) window.codeLock.lock('Modo texto ativo');

    if (!codeEditor.value || codeEditor.value.trim() === '') {
        try {
            if (typeof gerarCodigoPython === 'function') {
                const funcoes = typeof extrairFuncoesExistentes === 'function' ? extrairFuncoesExistentes() : {};
                const codigo = gerarCodigoPython(funcoes);
                codeEditor.value = codigo;
                codigoOriginal = codigo;
            }
        } catch(e) {
            logConsole("Erro ao gerar código base: " + e.message, "erro");
        }
    }
}

function GraphicMode() {
    const designer = document.getElementById("modoVisual");
    const editor = document.getElementById("modoTexto");
    const codeEditor = document.getElementById("codigoEditor");
    
    if (codeEditor) codigoOriginal = codeEditor.value;
    designer.style.display = "block";
    editor.style.display = "none";
    modoAtual = 'visual';
    
    if (window.codeLock) window.codeLock.unlock();
    
    if (codeEditor && codeEditor.value) {
        try {
            if (typeof importarPython === 'function') {
                importarPython(codeEditor.value);
            }
        } catch(e) {
            logConsole("Erro no Parser Gráfico: " + e.message, "erro");
        }
    }
}

function logConsole(mensagem, tipo = "info") {
    const consoleBox = document.getElementById("consoleOutput");
    if (!consoleBox) return;
    const timestamp = new Date().toLocaleTimeString();
    let prefix = `[${timestamp}] [INFO] `;
    if (tipo === "erro") prefix = `[${timestamp}] [ERROR] ❌ `;
    if (tipo === "success") prefix = `[${timestamp}] [SUCCESS] 🚀 `;
    
    consoleBox.innerHTML += prefix + mensagem + "\n";
    consoleBox.scrollTop = consoleBox.scrollHeight;
}

async function executarCodigoViaAPI(codigo, filename = 'script.py') {
    try {
        logConsole("Iniciando execução da aplicação...");
        const response = await fetch('/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: codigo, filename: filename, timeout: 30 })
        });
        const data = await response.json();
        if (data.success) {
            logConsole(`Execução concluída com sucesso.\nRetorno:\n${data.output || ''}`, "success");
        } else {
            logConsole(`Falha na execução:\n${data.error || ''}`, "erro");
        }
        return data;
    } catch (error) {
        logConsole("Erro ao conectar com o Servidor de Execução: " + error.message, "erro");
    }
}

async function compilarCodigoViaAPI(codigo, filename = 'script.py') {
    try {
        logConsole("Compilando binário executável autônomo (.exe)... (Pode demorar um minuto)");
        const response = await fetch('/compile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: codigo, filename: filename })
        });
        const data = await response.json();
        if (data.success) {
            logConsole(`Compilação concluída com sucesso! Salvo em: ${data.path || ''}`, "success");
        } else {
            logConsole(`Erro de compilação:\n${data.error || ''}`, "erro");
        }
        return data;
    } catch (error) {
        logConsole("Erro ao conectar com o Servidor de Compilação: " + error.message, "erro");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const editor = document.getElementById("codigoEditor");
    if (editor) {
        editor.removeAttribute("readonly");
        
        editor.addEventListener("focus", function() {
            this._usuarioDigitando = true;
            if (window.codeLock) {
                window.codeLock.detectManualEdit();
            }
        });
        
        editor.addEventListener("blur", function() {
            this._usuarioDigitando = false;
            codigoOriginal = this.value;
            if (window.codeLock) {
                if (this.value === window.codeLock.originalCode) {
                    window.codeLock.unlock();
                }
            }
        });
        
        editor.addEventListener("input", function() {
            codigoOriginal = this.value;
            if (window.codeLock) {
                window.codeLock.detectManualEdit();
                if (window.codeLock.locked) {
                    window.codeLock.syncEditor();
                }
            }
        });
    }
});

// Exporta funções globais
window.Visual = Visual;
window.GraphicMode = GraphicMode;
window.executarCodigoViaAPI = executarCodigoViaAPI;
window.compilarCodigoViaAPI = compilarCodigoViaAPI;
window.logConsole = logConsole;