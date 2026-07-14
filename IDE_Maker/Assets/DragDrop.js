// ============================================
// FALLBACK PARA FUNÇÕES FALTANTES
// ============================================

// Previne erro "abrirModoTexto is not defined"
if (typeof abrirModoTexto === 'undefined') {
    window.abrirModoTexto = function() {
        console.warn("abrirModoTexto chamado - redirecionando para Visual()");
        if (typeof Visual === 'function') {
            Visual();
        } else {
            const btn = document.getElementById('btnVisualMode');
            if (btn) btn.click();
        }
    };
}

// Previne erro "GraphicMode" se não existir
if (typeof GraphicMode === 'undefined') {
    window.GraphicMode = function() {
        console.warn("GraphicMode fallback");
        const btn = document.getElementById('btnGraphicMode');
        if (btn) btn.click();
    };
}

// ============================================
// REFERÊNCIAS DOM
// ============================================

const tools = document.querySelectorAll(".tool");
const canvas = document.getElementById("canvas");

let widgetSelecionado = null;
let widgetArrastando = null;
let offsetX = 0;
let offsetY = 0;
let arrastando = false;

// ============================================
// PROPRIEDADES PADRÃO DOS WIDGETS
// ============================================

const defaultProperties = {
    text: {
        x: 0, y: 0, width: 300, height: 150,
        text: "", bg: "#ffffff", fg: "#000000",
        hover_bg: "", pressed_bg: "", border_radius: 0,
        command: "", placeholder: "", min_value: 0, max_value: 100,
        value: "", items: "", orientation: "horizontal", url: ""
    },
    slider: {
        x: 0, y: 0, width: 180, height: 25,
        text: "", bg: "", fg: "",
        hover_bg: "", pressed_bg: "", border_radius: 0,
        command: "", placeholder: "", min_value: 0, max_value: 100,
        value: 50, items: "", orientation: "horizontal", url: ""
    },
    checkbox: {
        x: 0, y: 0, width: 20, height: 20,
        text: "Checkbox", bg: "", fg: "#000000",
        hover_bg: "", pressed_bg: "", border_radius: 0,
        command: "", placeholder: "", min_value: 0, max_value: 100,
        value: false, items: "", orientation: "horizontal", url: ""
    },
    button: {
        x: 0, y: 0, width: 120, height: 40,
        text: "Button", bg: "#4a90e2", fg: "#ffffff",
        hover_bg: "#5aa0f2", pressed_bg: "#3578c8",
        border_radius: 4, command: "", placeholder: "",
        min_value: 0, max_value: 100, value: "",
        items: "", orientation: "horizontal", url: ""
    },
    label: {
        x: 0, y: 0, width: 100, height: 30,
        text: "Label", bg: "", fg: "#000000",
        hover_bg: "", pressed_bg: "", border_radius: 0,
        command: "", placeholder: "", min_value: 0, max_value: 100,
        value: "", items: "", orientation: "horizontal", url: ""
    },
    entry: {
        x: 0, y: 0, width: 180, height: 30,
        text: "", bg: "#ffffff", fg: "#000000",
        hover_bg: "", pressed_bg: "", border_radius: 4,
        command: "", placeholder: "Digite aqui...",
        min_value: 0, max_value: 100, value: "",
        items: "", orientation: "horizontal", url: ""
    },
    progress: {
        x: 0, y: 0, width: 180, height: 20,
        text: "", bg: "", fg: "",
        hover_bg: "", pressed_bg: "", border_radius: 0,
        command: "", placeholder: "", min_value: 0, max_value: 100,
        value: 50, items: "", orientation: "horizontal", url: ""
    },
    combobox: {
        x: 0, y: 0, width: 180, height: 30,
        text: "", bg: "", fg: "",
        hover_bg: "", pressed_bg: "", border_radius: 4,
        command: "", placeholder: "", min_value: 0, max_value: 100,
        value: "", items: "Item 1,Item 2",
        orientation: "horizontal", url: ""
    },
    web: {
        x: 0, y: 0, width: 250, height: 150,
        text: "", bg: "", fg: "",
        hover_bg: "", pressed_bg: "", border_radius: 0,
        command: "", placeholder: "", min_value: 0, max_value: 100,
        value: "", items: "", orientation: "horizontal",
        url: "https://example.com"
    },
    frame: {
        x: 0, y: 0, width: 200, height: 120,
        text: "", bg: "#ffffff", fg: "",
        hover_bg: "", pressed_bg: "", border_radius: 0,
        command: "", placeholder: "", min_value: 0, max_value: 100,
        value: "", items: "", orientation: "horizontal", url: ""
    }
};

// ============================================
// PREENCHER TABELA DE PROPRIEDADES
// ============================================

function preencherTabela(widget) {
    if (!widget) return;
    
    const p = widget.properties;
    
    document.getElementById("x").value = p.x || 0;
    document.getElementById("y").value = p.y || 0;
    document.getElementById("width").value = p.width || 100;
    document.getElementById("height").value = p.height || 30;
    document.getElementById("text").value = p.text || "";
    document.getElementById("bg").value = p.bg || "";
    document.getElementById("fg").value = p.fg || "";
    document.getElementById("hover_bg").value = p.hover_bg || "";
    document.getElementById("pressed_bg").value = p.pressed_bg || "";
    document.getElementById("border_radius").value = p.border_radius || 0;
    document.getElementById("command").value = p.command || "";
    document.getElementById("placeholder").value = p.placeholder || "";
    document.getElementById("min_value").value = p.min_value || 0;
    document.getElementById("max_value").value = p.max_value || 100;
    document.getElementById("url").value = p.url || "";
    document.getElementById("value").value = p.value !== undefined ? p.value : "";
    document.getElementById("items").value = p.items || "";
    document.getElementById("orientation").value = p.orientation || "horizontal";
}

function preencherTabelaAtual() {
    if (widgetSelecionado) {
        preencherTabela(widgetSelecionado);
        return;
    }
    
    document.getElementById("WTitle").value = interfaceProperties.title;
    document.getElementById("x").value = 0;
    document.getElementById("y").value = 0;
    document.getElementById("width").value = interfaceProperties.width;
    document.getElementById("height").value = interfaceProperties.height;
    document.getElementById("text").value = "";
    document.getElementById("bg").value = interfaceProperties.bg;
    document.getElementById("fg").value = interfaceProperties.fg;
    document.getElementById("hover_bg").value = "";
    document.getElementById("pressed_bg").value = "";
    document.getElementById("border_radius").value = "";
    document.getElementById("command").value = "";
    document.getElementById("placeholder").value = "";
    document.getElementById("min_value").value = "";
    document.getElementById("max_value").value = "";
    document.getElementById("url").value = "";
    document.getElementById("value").value = "";
    document.getElementById("items").value = "";
    document.getElementById("orientation").value = "horizontal";
}

function atualizarPainel() {
    preencherTabelaAtual();
}

// ============================================
// DRAG DA PALETA PARA O CANVAS
// ============================================

tools.forEach(tool => {
    tool.addEventListener("dragstart", e => {
        e.dataTransfer.setData("widget", tool.dataset.widget);
    });
});

canvas.addEventListener("dragover", e => {
    e.preventDefault();
});

canvas.addEventListener("drop", e => {
    e.preventDefault();
    const tipo = e.dataTransfer.getData("widget");
    const rect = canvas.getBoundingClientRect();
    
    criarWidget(tipo, {
        x: Math.round(e.clientX - rect.left),
        y: Math.round(e.clientY - rect.top)
    });
});

canvas.addEventListener("mousedown", e => {
    if (e.target === canvas) {
        widgetSelecionado = null;
        preencherTabelaAtual();
        atualizarWidget();
    }
});

// ============================================
// TORNAR WIDGET MÓVEL
// ============================================

function tornarMovel(widget) {
    widget.addEventListener("mousedown", e => {
        e.stopPropagation();
        e.preventDefault();
        
        widgetSelecionado = widget;
        arrastando = true;
        
        const rect = widget.getBoundingClientRect();
        offsetX = e.clientX - rect.left;
        offsetY = e.clientY - rect.top;
        
        preencherTabelaAtual();
    });
}

document.addEventListener("mouseup", () => {
    arrastando = false;
});

document.addEventListener("mousemove", e => {
    if (!arrastando || !widgetSelecionado) return;
    
    const rect = canvas.getBoundingClientRect();
    let x = e.clientX - rect.left - offsetX;
    let y = e.clientY - rect.top - offsetY;
    
    x = Math.max(0, Math.min(x, canvas.clientWidth - widgetSelecionado.offsetWidth));
    y = Math.max(0, Math.min(y, canvas.clientHeight - widgetSelecionado.offsetHeight));
    
    widgetSelecionado.style.left = x + "px";
    widgetSelecionado.style.top = y + "px";
    widgetSelecionado.properties.x = x;
    widgetSelecionado.properties.y = y;
    
    preencherTabelaAtual();
});

// ============================================
// DUPLO CLIQUE PARA ABRIR EDITOR
// ============================================

function configurarDuploClique(widget) {
    widget.addEventListener("dblclick", () => {
        const cmd = widget.properties?.command;
        if (cmd && cmd.trim() !== "") {
            if (typeof abrirEditor === 'function') {
                abrirEditor(cmd.trim());
            } else {
                console.warn("Função abrirEditor não disponível");
            }
        }
    });
}

// ============================================
// ATUALIZAR WIDGET A PARTIR DA TABELA
// ============================================

function atualizarWidget() {
    if (!widgetSelecionado) {
        interfaceProperties.title = document.getElementById("WTitle").value || "Nova Interface";
        interfaceProperties.width = Number(document.getElementById("width").value) || 900;
        interfaceProperties.height = Number(document.getElementById("height").value) || 650;
        interfaceProperties.bg = document.getElementById("bg").value || "#ffffff";
        interfaceProperties.fg = document.getElementById("fg").value || "#000000";
        
        canvas.style.width = interfaceProperties.width + "px";
        canvas.style.height = interfaceProperties.height + "px";
        canvas.style.background = interfaceProperties.bg;
        canvas.style.color = interfaceProperties.fg;
        document.title = interfaceProperties.title;
        
        if (typeof atualizarCodigoEditor === "function") {
            try {
                atualizarCodigoEditor();
            } catch(e) {
                console.warn("Erro ao atualizar editor:", e);
            }
        }
        return;
    }
    
    const p = widgetSelecionado.properties;
    
    p.x = Number(document.getElementById("x").value) || 0;
    p.y = Number(document.getElementById("y").value) || 0;
    p.width = Number(document.getElementById("width").value) || 100;
    p.height = Number(document.getElementById("height").value) || 30;
    p.text = document.getElementById("text").value || "";
    p.bg = document.getElementById("bg").value || "";
    p.fg = document.getElementById("fg").value || "";
    p.hover_bg = document.getElementById("hover_bg").value || "";
    p.pressed_bg = document.getElementById("pressed_bg").value || "";
    p.border_radius = Number(document.getElementById("border_radius").value) || 0;
    p.command = document.getElementById("command").value || "";
    p.placeholder = document.getElementById("placeholder").value || "";
    p.min_value = Number(document.getElementById("min_value").value) || 0;
    p.max_value = Number(document.getElementById("max_value").value) || 100;
    p.url = document.getElementById("url").value || "";
    p.value = document.getElementById("value").value;
    p.items = document.getElementById("items").value || "";
    p.orientation = document.getElementById("orientation").value || "horizontal";
    
    aplicarProperties(widgetSelecionado);
    
    if (typeof atualizarCodigoEditor === "function") {
        try {
            atualizarCodigoEditor();
        } catch(e) {
            console.warn("Erro ao atualizar editor:", e);
        }
    }
}

// ============================================
// APLICAR PROPRIEDADES AO WIDGET
// ============================================

function aplicarProperties(widget) {
    const p = widget.properties;
    
    if (!p.name) {
        p.name = gerarNomeWidget(widget.dataset.tipo);
    }
    
    widget.style.left = p.x + "px";
    widget.style.top = p.y + "px";
    widget.style.width = p.width + "px";
    widget.style.height = p.height + "px";
    
    if (p.bg && p.bg !== "") {
        widget.style.background = p.bg;
    }
    if (p.fg && p.fg !== "") {
        widget.style.color = p.fg;
    }
    if (p.border_radius !== undefined) {
        widget.style.borderRadius = p.border_radius + "px";
    }
    
    switch (widget.dataset.tipo) {
        case "label":
            widget.textContent = p.text || "";
            break;
            
        case "button":
            widget.textContent = p.text || "";
            if (p.hover_bg) {
                widget.addEventListener("mouseenter", () => {
                    widget.style.background = p.hover_bg;
                });
                widget.addEventListener("mouseleave", () => {
                    widget.style.background = p.bg || "#4a90e2";
                });
            }
            if (p.pressed_bg) {
                widget.addEventListener("mousedown", () => {
                    widget.style.background = p.pressed_bg;
                });
                widget.addEventListener("mouseup", () => {
                    widget.style.background = p.bg || "#4a90e2";
                });
            }
            break;
            
        case "entry":
            widget.placeholder = p.placeholder || "";
            widget.value = p.value || "";
            break;
            
        case "slider":
            widget.min = Number(p.min_value) || 0;
            widget.max = Number(p.max_value) || 100;
            widget.value = Number(p.value) || 0;
            if (p.orientation === "vertical") {
                widget.style.transform = "rotate(90deg)";
            } else {
                widget.style.transform = "";
            }
            break;
            
        case "progress":
            widget.max = Number(p.max_value) || 100;
            widget.value = Number(p.value) || 0;
            break;
            
        case "checkbox":
            widget.checked = Boolean(p.value);
            const label = document.createElement("span");
            label.textContent = p.text || "Checkbox";
            if (widget.parentNode) {
                widget.parentNode.insertBefore(label, widget.nextSibling);
            }
            break;
            
        case "combobox":
            widget.innerHTML = "";
            let lista = p.items;
            if (typeof lista === "string") {
                lista = lista.split(",").map(item => item.trim());
            }
            if (Array.isArray(lista)) {
                lista.forEach(item => {
                    const option = document.createElement("option");
                    option.textContent = item;
                    widget.appendChild(option);
                });
            }
            break;
            
        case "web":
            widget.src = p.url || "";
            break;
            
        case "frame":
            if (p.bg) {
                widget.style.background = p.bg;
            }
            break;
    }
}

// ============================================
// CRIAR WIDGET
// ============================================

function criarWidget(tipo, properties = {}) {
    let novo;
    
    switch (tipo) {
        case "slider":
            novo = document.createElement("input");
            novo.type = "range";
            break;
        case "checkbox":
            novo = document.createElement("input");
            novo.type = "checkbox";
            break;
        case "label":
            novo = document.createElement("label");
            break;
        case "entry":
            novo = document.createElement("input");
            novo.type = "text";
            break;
        case "text":
            novo = document.createElement("textarea");
            break;
        case "progress":
            novo = document.createElement("progress");
            break;
        case "combobox":
            novo = document.createElement("select");
            break;
        case "button":
            novo = document.createElement("button");
            break;
        case "web":
            novo = document.createElement("iframe");
            break;
        case "frame":
            novo = document.createElement("div");
            break;
        default:
            console.error("Widget desconhecido:", tipo);
            return null;
    }
    
    novo.classList.add("widget");
    novo.dataset.tipo = tipo;
    
    const defaults = defaultProperties[tipo] || {};
    novo.properties = {
        ...structuredClone(defaults),
        ...properties
    };
    
    if (!novo.properties.name) {
        novo.properties.name = gerarNomeWidget(tipo);
    }
    
    novo.style.position = "absolute";
    novo.style.border = "2px solid #666";
    novo.style.boxSizing = "border-box";
    
    canvas.appendChild(novo);
    aplicarProperties(novo);
    tornarMovel(novo);
    configurarDuploClique(novo);
    
    widgetSelecionado = novo;
    preencherTabelaAtual();
    
    if (typeof atualizarCodigoEditor === "function") {
        try {
            atualizarCodigoEditor();
        } catch(e) {
            console.warn("Erro ao atualizar editor:", e);
        }
    }
    
    return novo;
}

// ============================================
// REMOVER WIDGET SELECIONADO
// ============================================

function removerWidgetSelecionado() {
    if (!widgetSelecionado) {
        alert("Nenhum elemento selecionado.");
        return;
    }
    
    widgetSelecionado.remove();
    widgetSelecionado = null;
    preencherTabelaAtual();
    
    if (typeof atualizarCodigoEditor === "function") {
        try {
            atualizarCodigoEditor();
        } catch(e) {
            console.warn("Erro ao atualizar editor:", e);
        }
    }
}

document.getElementById("deleteWidget").addEventListener("click", removerWidgetSelecionado);

// ============================================
// LIMPAR CANVAS
// ============================================

function limparCanvas() {
    canvas.querySelectorAll(".widget").forEach(w => w.remove());
    widgetSelecionado = null;
}

// ============================================
// EVENTOS DA TABELA
// ============================================

document.querySelectorAll(".Propperties input, .Propperties select").forEach(campo => {
    campo.addEventListener("input", atualizarWidget);
    campo.addEventListener("change", atualizarWidget);
});

// ============================================
// INICIALIZAÇÃO
// ============================================

window.modoAtual = 'visual';

canvas.style.width = interfaceProperties.width + "px";
canvas.style.height = interfaceProperties.height + "px";
canvas.style.background = interfaceProperties.bg;
document.title = interfaceProperties.title;

preencherTabelaAtual();

const editor = document.getElementById("codigoEditor");
if (editor) {
    editor._usuarioDigitando = false;
    if (typeof gerarCodigoPython === 'function') {
        try {
            const codigo = gerarCodigoPython();
            editor.value = codigo;
        } catch(e) {
            console.warn("Erro ao gerar código inicial:", e);
            editor.value = "# Código Python gerado aqui";
        }
    } else {
        console.warn("Função gerarCodigoPython não disponível");
        editor.value = "# Código Python gerado aqui";
    }
}

// ============================================
// FUNÇÃO DE FALLBACK PARA ABRIR EDITOR
// ============================================

if (typeof abrirEditor === 'undefined') {
    window.abrirEditor = function(nomeFuncao) {
        console.log("Função abrirEditor (fallback):", nomeFuncao);
        const btnVisual = document.getElementById("btnVisualMode");
        if (btnVisual) {
            btnVisual.click();
        }
        const editor = document.getElementById("codigoEditor");
        if (editor) {
            editor.focus();
            const texto = editor.value;
            const posicao = texto.indexOf("def " + nomeFuncao);
            if (posicao !== -1) {
                editor.setSelectionRange(posicao, posicao);
            }
        }
    };
}