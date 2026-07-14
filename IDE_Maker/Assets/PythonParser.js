// PythonParser.js - Atualizado para novas funcionalidades

window.importarPython = function(codigo) {
    console.log("Importando codigo para o visual...");
    
    const funcoesExtraidas = {};
    const regexFuncao = /def\s+(\w+)\s*\([^)]*\)\s*:([\s\S]*?)(?=\n\S|$)/g;
    let match;
    
    while ((match = regexFuncao.exec(codigo)) !== null) {
        const nome = match[1];
        let corpo = match[2];
        corpo = corpo.replace(/^    /gm, '');
        funcoesExtraidas[nome] = corpo.trim();
    }
    
    console.log("Funcoes extraidas:", Object.keys(funcoesExtraidas));
    
    const gui = codigo.match(/gui\s*=\s*GuiSpark\s*\(([\s\S]*?)\)/);
    
    if (gui) {
        let bloco = gui[1];
        
        let title = bloco.match(/title\s*=\s*"([^"]*)"/);
        let width = bloco.match(/width\s*=\s*(\d+)/);
        let height = bloco.match(/height\s*=\s*(\d+)/);
        
        if (title) interfaceProperties.title = title[1];
        if (width) interfaceProperties.width = Number(width[1]);
        if (height) interfaceProperties.height = Number(height[1]);
    }
    
    canvas.style.width = interfaceProperties.width + "px";
    canvas.style.height = interfaceProperties.height + "px";
    document.title = interfaceProperties.title;
    
    limparCanvas();
    
    const regex = /(?:(\w+)\s*=\s*)?gui\.add_widget\s*\(\s*["']([^"']+)["']\s*([\s\S]*?)\)/g;
    let resultado;
    let contador = 0;
    
    while ((resultado = regex.exec(codigo)) !== null) {
        contador++;
        
        let nome = resultado[1];
        let tipo = resultado[2];
        let params = resultado[3];
        
        if (!nome) {
            nome = tipo + "_" + contador;
        }
        
        function pegar(campo) {
            const regex = new RegExp(campo + "\\s*=\\s*([^,\\n]+)", "i");
            const r = params.match(regex);
            
            if (!r) return "";
            
            let valor = r[1].trim();
            
            if (valor.startsWith('"') && valor.endsWith('"')) {
                return valor.slice(1, -1);
            }
            if (valor.startsWith("'") && valor.endsWith("'")) {
                return valor.slice(1, -1);
            }
            
            if (valor.startsWith("[") && valor.endsWith("]")) {
                try {
                    return JSON.parse(valor.replaceAll("'", '"'));
                } catch {
                    return [];
                }
            }
            
            if (valor === "True" || valor === "true") return true;
            if (valor === "False" || valor === "false") return false;
            if (valor === "None" || valor === "null") return "";
            
            if (!isNaN(valor) && valor !== "") return Number(valor);
            
            return valor;
        }
        
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
        
        criarWidget(tipo, props);
    }
    
    console.log("Importacao finalizada, widgets criados:", contador);
    
    const editor = document.getElementById("codigoEditor");
    if (editor) {
        const funcoesParaPreservar = funcoesExtraidas;
        const novoCodigo = gerarCodigoPython(funcoesParaPreservar);
        editor.value = novoCodigo;
    }
};