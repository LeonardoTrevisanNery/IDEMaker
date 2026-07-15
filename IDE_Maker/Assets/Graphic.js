// ============================================
// GRAPHIC.JS - PROPRIEDADES BASE DA INTERFACE
// ============================================

const interfaceProperties = {
    title: "Nova Interface",
    width: 900,
    height: 650,
    bg: "#ffffff",
    fg: "#000000"
};

// ============================================
// CONTROLE DE TEMA
// ============================================

let temaAtual = null;
let customTheme = {
    bg: "#ffffff",
    fg: "#000000",
    widget_bg: "#f0f0f0",
    widget_fg: "#000000",
    accent: "#af72fa"
};

// ============================================
// CONTADOR DE WIDGETS
// ============================================

let widgetCounter = 0;

function gerarNomeWidget(tipo) {
    widgetCounter++;
    return tipo + "_" + widgetCounter;
}

// ============================================
// EXTRAIR FUNÇÕES EXISTENTES DO EDITOR
// ============================================

function extrairFuncoesExistentes() {
    const editor = document.getElementById("codigoEditor");
    const funcoes = {};
    
    if (editor && editor.value) {
        const codigo = editor.value;
        const regexFuncao = /def\s+(\w+)\s*\([^)]*\)\s*:([\s\S]*?)(?=\n\s*def\s+|\n\s*#\s*={10,}|\n\s*$|$)/g;
        let match;
        while ((match = regexFuncao.exec(codigo)) !== null) {
            const nome = match[1];
            let corpo = match[2];
            const linhas = corpo.split('\n');
            if (linhas.length > 0) {
                const primeiraLinha = linhas[0];
                const matchIndent = primeiraLinha.match(/^(\s+)/);
                if (matchIndent) {
                    const indent = matchIndent[1];
                    corpo = linhas.map(l => l.startsWith(indent) ? l.substring(indent.length) : l).join('\n');
                }
            }
            funcoes[nome] = corpo;
        }
    }
    return funcoes;
}

// ============================================
// ATUALIZAÇÃO SEGURA DO PAINEL DE PROPRIEDADES
// ============================================

function preencherTabelaAtual() {
    if (!window.widgetSelecionado) {
        const campos = ["WTitle", "width", "height", "x", "y", "text", "bg", "fg", "command", "items"];
        campos.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = "";
        });
        return;
    }

    const p = window.widgetSelecionado.properties || {};

    const definirValor = (id, valor) => {
        const el = document.getElementById(id);
        if (el) el.value = valor !== undefined && valor !== null ? valor : "";
    };

    definirValor("width", window.widgetSelecionado.offsetWidth || p.width);
    definirValor("height", window.widgetSelecionado.offsetHeight || p.height);
    definirValor("x", window.widgetSelecionado.offsetLeft || p.x);
    definirValor("y", window.widgetSelecionado.offsetTop || p.y);
    definirValor("text", p.text);
    definirValor("bg", p.bg);
    definirValor("fg", p.fg);
    definirValor("command", p.command);
    definirValor("items", p.items);
}

function atualizarWidget() {
    const pegarValor = (id) => {
        const el = document.getElementById(id);
        return el ? el.value : "";
    };

    // ============================================================
    // CASO 1: SE HOUVER WIDGET SELECIONADO (Atualiza o componente)
    // ============================================================
    if (window.widgetSelecionado) {
        window.widgetSelecionado.properties.text = pegarValor("text");
        window.widgetSelecionado.properties.bg = pegarValor("bg");
        window.widgetSelecionado.properties.fg = pegarValor("fg");
        window.widgetSelecionado.properties.command = pegarValor("command");
        window.widgetSelecionado.properties.items = pegarValor("items");

        const newWidth = Number(pegarValor("width"));
        const newHeight = Number(pegarValor("height"));
        const newX = Number(pegarValor("x"));
        const newY = Number(pegarValor("y"));

        if (!isNaN(newWidth)) window.widgetSelecionado.style.width = newWidth + "px";
        if (!isNaN(newHeight)) window.widgetSelecionado.style.height = newHeight + "px";
        if (!isNaN(newX)) window.widgetSelecionado.style.left = newX + "px";
        if (!isNaN(newY)) window.widgetSelecionado.style.top = newY + "px";

        const render = window.widgetSelecionado.querySelector('.widget-text-render');
        if (render) {
            render.innerText = window.widgetSelecionado.properties.text !== undefined && window.widgetSelecionado.properties.text !== "" 
                ? window.widgetSelecionado.properties.text 
                : window.widgetSelecionado.id;
        }
    } 
    // ============================================================
    // CASO 2: SE NÃO HOUVER SELEÇÃO (Atualiza os dados da tela/canvas)
    // ============================================================
    else {
        if (!window.interfaceProperties) {
            window.interfaceProperties = { title: "Nova Interface", width: 900, height: 650, bg: "#121212", fg: "#e0e0e0" };
        }

        window.interfaceProperties.title = pegarValor("WTitle") || "Nova Interface";
        window.interfaceProperties.width = Number(pegarValor("width")) || 900;
        window.interfaceProperties.height = Number(pegarValor("height")) || 650;
        window.interfaceProperties.bg = pegarValor("bg") || "#121212";
        window.interfaceProperties.fg = pegarValor("fg") || "#e0e0e0";

        // Ajusta o tamanho fidedigno do canvas de acordo com os inputs
        const canvasEl = document.getElementById("canvas");
        if (canvasEl) {
            canvasEl.style.width = window.interfaceProperties.width + "px";
            canvasEl.style.height = window.interfaceProperties.height + "px";
            canvasEl.style.background = window.interfaceProperties.bg;
            canvasEl.style.color = window.interfaceProperties.fg;
        }
    }

    // Sincroniza o código gerado no editor em ambos os cenários
    if (typeof atualizarCodigoEditor === 'function') {
        atualizarCodigoEditor();
    }
}

function atualizarCodigoEditor() {
    const editor = document.getElementById("codigoEditor");
    if (editor) {
        try {
            const funcoes = typeof extrairFuncoesExistentes === 'function' ? extrairFuncoesExistentes() : {};
            if (typeof gerarCodigoPython === 'function') {
                editor.value = gerarCodigoPython(funcoes);
            }
        } catch (e) {
            console.warn("Erro ao sincronizar editor:", e);
        }
    }
}

function colocarCodigoNoEditor() {
    const editor = document.getElementById("codigoEditor");
    if (editor && editor.value) {
        try {
            if (typeof importarPython === 'function') {
                importarPython(editor.value);
            }
        } catch (e) {
            console.error("Erro ao importar:", e);
            if (typeof logConsole === 'function') {
                logConsole("Erro ao importar o código. Verifique a sintaxe.", "erro");
            } else {
                alert("Erro ao importar o código. Verifique a sintaxe.");
            }
        }
    }
}

// ============================================
// GERAR CÓDIGO BASE
// ============================================

function gerarCodigoBase() {
    return `from Assets.Core.Base import GuiSpark

gui = GuiSpark(
    title="${interfaceProperties.title}",
    width=${interfaceProperties.width},
    height=${interfaceProperties.height}
)

# gui.set_theme("dark")  # Descomente para ativar o tema escuro

# ===========================
# Funções
# ===========================

# Defina suas funções aqui

# ===========================
# Widgets
# ===========================

# Adicione seus widgets aqui

gui.run()
`;
}



// ============================================================
// PREENCHE A TABELA COM AS PROPRIEDADES DA TELA/INTERFACE
// ============================================================
function preencherTabelaInterface() {
    // Garante que o ID "WTitle" e outros campos recebam as propriedades globais da janela
    const definirValor = (id, valor) => {
        const el = document.getElementById(id);
        if (el) el.value = valor !== undefined && valor !== null ? valor : "";
    };

    definirValor("WTitle", window.interfaceProperties?.title);
    definirValor("width", window.interfaceProperties?.width);
    definirValor("height", window.interfaceProperties?.height);
    definirValor("bg", window.interfaceProperties?.bg);
    definirValor("fg", window.interfaceProperties?.fg);

    // Limpa campos que pertencem exclusivamente a widgets individuais
    const camposDeWidget = ["x", "y", "text", "command", "items"];
    camposDeWidget.forEach(id => definirValor(id, ""));
}

// Expõe a função globalmente para ser chamada pelo DragDrop.js
window.preencherTabelaInterface = preencherTabelaInterface;

// ============================================
// EXPORTA FUNÇÕES GLOBAIS
// ============================================

window.gerarNomeWidget = gerarNomeWidget;
window.extrairFuncoesExistentes = extrairFuncoesExistentes;
window.atualizarCodigoEditor = atualizarCodigoEditor;
window.colocarCodigoNoEditor = colocarCodigoNoEditor;
window.preencherTabelaAtual = preencherTabelaAtual;
window.atualizarWidget = atualizarWidget;

// ============================================
// INICIALIZAÇÃO DO TAMANHO DO CANVAS
// ============================================
// Garante que o canvas aplique o tamanho correto (ex: 900x650 ou o que estiver definido) logo que a página carregar
if (typeof atualizarTamanhoCanvas === "function") {
    atualizarTamanhoCanvas();
} else {
    // Fallback caso a função atualizarTamanhoCanvas ainda não tenha sido declarada no escopo
    const canvasEl = document.getElementById("canvas");
    if (canvasEl && window.interfaceProperties) {
        canvasEl.style.width = window.interfaceProperties.width + "px";
        canvasEl.style.height = window.interfaceProperties.height + "px";
        canvasEl.style.background = window.interfaceProperties.bg || "#121212";
    }
}
