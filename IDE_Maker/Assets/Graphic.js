// ============================================
// PROPRIEDADES BASE DA INTERFACE
// ============================================

const interfaceProperties = {
    title: "Nova Interface",
    width: 900,
    height: 650,
    bg: "#ffffff",
    fg: "#000000"
};

// ============================================
// CONTROLE DE TEMA - CORRIGIDO
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
        const regexFuncao = /def\s+(\w+)\s*\([^)]*\)\s*:([\s\S]*?)(?=\n\S|$)/g;
        let match;
        
        while ((match = regexFuncao.exec(codigo)) !== null) {
            const nome = match[1];
            let corpo = match[2];
            corpo = corpo.replace(/^    /gm, '');
            funcoes[nome] = corpo.trim();
        }
    }
    
    return funcoes;
}

// ============================================
// ATUALIZAR CÓDIGO NO EDITOR
// ============================================

function atualizarCodigoEditor() {
    const editor = document.getElementById("codigoEditor");
    if (!editor) return;
    
    try {
        const funcoesPersonalizadas = extrairFuncoesExistentes();
        const codigo = gerarCodigoPython(funcoesPersonalizadas);
        editor.value = codigo;
    } catch (e) {
        console.error("Erro ao gerar código:", e);
    }
}

function colocarCodigoNoEditor(codigo) {
    const editor = document.getElementById("codigoEditor");
    if (!editor) return;
    editor.value = codigo;
}

// ============================================
// FUNÇÕES DE NAVEGAÇÃO ENTRE MODOS
// ============================================

function abrirModoTexto() {
    const visual = document.getElementById("modoVisual");
    const texto = document.getElementById("modoTexto");
    
    if (visual) visual.style.display = "none";
    if (texto) texto.style.display = "flex";
    
    const funcoesPersonalizadas = extrairFuncoesExistentes();
    const codigo = gerarCodigoPython(funcoesPersonalizadas);
    colocarCodigoNoEditor(codigo);
}

function fecharModoTexto() {
    const visual = document.getElementById("modoVisual");
    const texto = document.getElementById("modoTexto");
    
    if (visual) visual.style.display = "block";
    if (texto) texto.style.display = "none";
    
    const editor = document.getElementById("codigoEditor");
    if (editor && editor.value) {
        try {
            importarPython(editor.value);
        } catch (e) {
            console.error("Erro ao importar:", e);
            alert("Erro ao importar o código. Verifique a sintaxe.");
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

// ============================================
// EXPORTA FUNÇÕES GLOBAIS
// ============================================

window.gerarNomeWidget = gerarNomeWidget;
window.extrairFuncoesExistentes = extrairFuncoesExistentes;
window.atualizarCodigoEditor = atualizarCodigoEditor;
window.colocarCodigoNoEditor = colocarCodigoNoEditor;
window.abrirModoTexto = abrirModoTexto;
window.fecharModoTexto = fecharModoTexto;
window.gerarCodigoBase = gerarCodigoBase;
window.temaAtual = temaAtual;
window.customTheme = customTheme;