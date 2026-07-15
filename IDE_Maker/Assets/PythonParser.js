// ============================================
// PARSER PYTHON PARA VISUALIZAÇÃO
// ============================================

let funcoesExtraidas = {};
let ultimoCodigoParseado = '';
let parseando = false;

function importarPython(codigo) {
    if (parseando) {
        console.log('⏳ Já está parseando... ignorando');
        return;
    }
    
    if (codigo === ultimoCodigoParseado) {
        console.log('📝 Código já parseado, ignorando...');
        return;
    }
    
    console.log("📝 Parser iniciado");
    parseando = true;
    ultimoCodigoParseado = codigo;
    
    if (!codigo || typeof codigo !== "string") {
        console.warn("Código inválido para parser");
        parseando = false;
        return;
    }
    
    // ============================================
    // EXTRAI FUNÇÕES (preservando indentação)
    // ============================================
    
    funcoesExtraidas = {};
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
        funcoesExtraidas[nome] = corpo;
    }

    // ============================================
    // PARSE DAS CONFIGURAÇÕES DA JANELA PRINCIPAL
    // ============================================
    const regexGui = /gui\s*=\s*GuiSpark\s*\(\s*title\s*=\s*["']([^"']+)["']\s*,\s*width\s*=\s*(\d+)\s*,\s*height\s*=\s*(\d+)\s*\)/;
    const matchGui = codigo.match(regexGui);

    if (matchGui && window.interfaceProperties) {
        window.interfaceProperties.title = matchGui[1];
        window.interfaceProperties.width = Number(matchGui[2]);
        window.interfaceProperties.height = Number(matchGui[3]);
        
        const inputTitle = document.getElementById("WTitle");
        if (inputTitle) inputTitle.value = window.interfaceProperties.title;
        
        const inputWidth = document.getElementById("width");
        if (inputWidth && !window.widgetSelecionado) inputWidth.value = window.interfaceProperties.width;
        
        const inputHeight = document.getElementById("height");
        if (inputHeight && !window.widgetSelecionado) inputHeight.value = window.interfaceProperties.height;
    }

    // Parse do tema
    const temaMatch = codigo.match(/gui\.set_theme\s*\(\s*["']([^"']+)["']\s*\)/);
    if (temaMatch) {
        window.temaAtual = temaMatch[1];
    }

    // ============================================
    // RECONSTRUÇÃO DOS WIDGETS NO CANVAS
    // ============================================
    const canvas = document.getElementById("canvas");
    if (!canvas) {
        console.warn("Canvas não encontrado no DOM.");
        parseando = false;
        return;
    }

    // Limpa o canvas antigo antes de renderizar
    canvas.innerHTML = "";
    
    // Mapeia chamadas: nome = gui.add_widget("tipo", ...)
    const regexWidget = /(\w+)\s*=\s*gui\.add_widget\s*\(\s*["']([^"']+)["']\s*,\s*([\s\S]*?)(?=\)\s*\n|\)$)/g;
    let matchW;
    
    while ((matchW = regexWidget.exec(codigo)) !== null) {
        const nome = matchW[1];
        const tipo = matchW[2];
        const paramsStr = matchW[3];
        
        const pegar = (campo) => {
            const r = new RegExp(campo + '\\s*=\\s*(["\'])(.*?)\\1');
            const m = paramsStr.match(r);
            if (m) return m[2];
            
            const rNum = new RegExp(campo + '\\s*=\\s*([^,\\n\\s]+)');
            const mNum = paramsStr.match(rNum);
            if (mNum) {
                let valor = mNum[1].trim();
                if (valor.startsWith("[") && valor.endsWith("]")) {
                    try { return JSON.parse(valor.replaceAll("'", '"')); } catch { return []; }
                }
                if (valor === "True" || valor === "true") return true;
                if (valor === "False" || valor === "false") return false;
                if (valor === "None" || valor === "null") return "";
                if (!isNaN(valor) && valor !== "") return Number(valor);
                return valor;
            }
            return "";
        };
        
        let props = {
            name: nome,
            x: Number(pegar("x")) || 0,
            y: Number(pegar("y")) || 0,
            width: Number(pegar("width")) || 100,
            height: Number(pegar("height")) || 30,
            text: pegar("text"),
            bg: pegar("bg"),
            fg: pegar("fg"),
            hover_bg: pegar("hover_bg"),
            pressed_bg: pegar("pressed_bg"),
            border_radius: Number(pegar("border_radius")) || 0,
            command: pegar("command"),
            placeholder: pegar("placeholder"),
            url: pegar("url"),
            min_value: Number(pegar("min_value")) || 0,
            max_value: Number(pegar("max_value")) || 100,
            value: pegar("value"),
            items: pegar("items"),
            orientation: pegar("orientation") || "horizontal"
        };
        
        if (typeof criarWidget === 'function') {
            criarWidget(tipo, props);
        } else {
            const div = document.createElement("div");
            div.className = "widget";
            div.id = nome;
            div.dataset.tipo = tipo;
            div.style.position = "absolute";
            div.style.left = props.x + "px";
            div.style.top = props.y + "px";
            div.style.width = props.width + "px";
            div.style.height = props.height + "px";
            div.properties = props;
            
            const txtRender = document.createElement("span");
            txtRender.className = "widget-text-render";
            txtRender.innerText = props.text !== undefined ? props.text : nome;
            div.appendChild(txtRender);
            
            canvas.appendChild(div);
        }
    }
    
    const ids = Array.from(canvas.querySelectorAll(".widget")).map(w => parseInt(w.id.split("_")[1])).filter(id => !isNaN(id));
    if (ids.length > 0) {
        window.widgetCounter = Math.max(...ids);
    }
    
    parseando = false;
    console.log("✅ Parser concluído com sucesso");
}

window.importarPython = importarPython;
window.funcoesExtraidas = funcoesExtraidas;