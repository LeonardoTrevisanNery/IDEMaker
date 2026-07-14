// ============================================
// FUNÇÕES DO EDITOR - ESTILO CODEBLOCKS
// ============================================

function abrirEditor(nomeFuncao) {
    // Extrai funções personalizadas antes de abrir
    const funcoesPersonalizadas = extrairFuncoesExistentes();
    
    // Abre o modo texto
    abrirModoTexto();
    
    // Posiciona o cursor na função
    setTimeout(() => {
        posicionarCursorNaFuncao(nomeFuncao);
    }, 100);
}

function posicionarCursorNaFuncao(nomeFuncao) {
    const editor = document.getElementById("codigoEditor");
    if (!editor) {
        console.error("Editor não encontrado");
        return;
    }

    const texto = editor.value;
    const posicao = texto.indexOf("def " + nomeFuncao);

    if (posicao === -1) {
        console.warn("Função não encontrada:", nomeFuncao);
        return;
    }

    editor.focus();
    editor.setSelectionRange(posicao, posicao);
    
    // Scroll para a posição
    const lines = texto.substring(0, posicao).split('\n');
    const lineNumber = lines.length;
    const lineHeight = 20; // Aproximado
    editor.scrollTop = lineNumber * lineHeight;
}

// ============================================
// SALVAR CÓDIGO PERSONALIZADO
// ============================================

function salvarCodigoPersonalizado() {
    const editor = document.getElementById("codigoEditor");
    if (!editor || !editor.value) return;
    
    // Extrai funções do código atual para preservar
    const funcoes = extrairFuncoesExistentes();
    
    // Atualiza o código mantendo as funções
    const novoCodigo = gerarCodigoPython(funcoes);
    editor.value = novoCodigo;
}

// ============================================
// EXPORTA FUNÇÕES
// ============================================

window.abrirEditor = abrirEditor;
window.posicionarCursorNaFuncao = posicionarCursorNaFuncao;
window.salvarCodigoPersonalizado = salvarCodigoPersonalizado;