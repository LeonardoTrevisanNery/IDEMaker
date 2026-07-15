// ============================================
// DRAGDROP.JS - IDE STYLE CODEBLOCKS (CORRIGIDO)
// ============================================

const canvas = document.getElementById("canvas");
const tools = document.querySelectorAll(".tool");

let widgetSelecionado = null;
let widgetArrastando = null;
let offsetX = 0;
let offsetY = 0;
let arrastando = false;

// Configurações padrão de propriedades por tipo de Widget
const defaultProperties = {
    button: { text: "Botão", width: 120, height: 40, bg: "#007acc", fg: "#ffffff", command: "ao_clicar" },
    label: { text: "Texto de Exibição", width: 150, height: 30, bg: "transparent", fg: "#ffffff", command: "" },
    entry: { text: "", width: 160, height: 35, bg: "#333333", fg: "#ffffff", placeholder: "Digite aqui...", command: "" },
    checkbox: { text: "Opção", width: 120, height: 30, bg: "transparent", fg: "#ffffff", value: false, command: "" },
    slider: { width: 180, height: 35, min_value: 0, max_value: 100, value: 50, orientation: "horizontal", command: "" },
    progress: { width: 180, height: 30, value: 30, bg: "#333333", fg: "#007acc" },
    combobox: { width: 160, height: 35, items: "Opção 1,Opção 2", command: "" },
    frame: { text: "", width: 250, height: 180, bg: "#2d2d2d", fg: "#ffffff" }
};

// Configuração da Paleta Esquerda
tools.forEach(tool => {
    tool.addEventListener("dragstart", (e) => {
        e.dataTransfer.setData("text/plain", tool.dataset.widget);
    });
});

if (canvas) {
    canvas.addEventListener("dragover", (e) => {
        e.preventDefault();
    });

    canvas.addEventListener("drop", (e) => {
        e.preventDefault();
        const tipo = e.dataTransfer.getData("text/plain");
        if (!tipo) return;

        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const nomeUnico = typeof gerarNomeWidget === "function" ? gerarNomeWidget(tipo) : tipo + "_" + Date.now();
        
        const props = Object.assign({
            name: nomeUnico,
            x: Math.round(x),
            y: Math.round(y),
        }, defaultProperties[tipo] || { text: tipo, width: 100, height: 30 });

        criarWidget(tipo, props);
    });

    // Deselecionar apenas quando clicar no fundo vazio do Canvas
    // Deselecionar widgets e focar nas propriedades da tela ao clicar no fundo vazio (Requisito 2)
    canvas.addEventListener("mousedown", (e) => {
        if (e.target === canvas) {
            deselecionarTodos();
            if (typeof preencherTabelaInterface === "function") {
                preencherTabelaInterface();
            }
        }
    });
}

// Função Principal de Criação de Elementos Visuais
function criarWidget(tipo, props) {
    if (!canvas) return;

    const div = document.createElement("div");
    div.className = "widget";
    div.id = props.name;
    div.dataset.tipo = tipo;
    
    // Dimensionamento real baseado nos pixels exatos
    div.style.position = "absolute";
    div.style.left = props.x + "px";
    div.style.top = props.y + "px";
    div.style.width = props.width + "px";
    div.style.height = props.height + "px";
    
    if (props.bg && props.bg !== "transparent") div.style.backgroundColor = props.bg;
    if (props.fg) div.style.color = props.fg;

    div.properties = props;

    // Renderizador de texto interno
    const txtRender = document.createElement("span");
    txtRender.className = "widget-text-render";
    txtRender.innerText = props.text !== undefined ? props.text : props.name;
    div.appendChild(txtRender);

    // Captura o clique e arrasto no componente
    div.addEventListener("mousedown", (e) => {
        e.preventDefault();
        e.stopPropagation(); // Impede o clique de passar para o canvas de fundo
        
        selecionarWidget(div);
        
        arrastando = true;
        widgetArrastando = div;
        offsetX = e.clientX - div.offsetLeft;
        offsetY = e.clientY - div.offsetTop;
    });

    canvas.appendChild(div);
    selecionarWidget(div);
}

// Controle de Movimentação do Mouse pelo Canvas
window.addEventListener("mousemove", (e) => {
    if (!arrastando || !widgetArrastando || !canvas) return;

    const rect = canvas.getBoundingClientRect();
    let newX = e.clientX - offsetX;
    let newY = e.clientY - offsetY;

    // Limites de movimentação reais
    if (newX < 0) newX = 0;
    if (newY < 0) newY = 0;
    if (newX + widgetArrastando.offsetWidth > rect.width) newX = rect.width - widgetArrastando.offsetWidth;
    if (newY + widgetArrastando.offsetHeight > rect.height) newY = rect.height - widgetArrastando.offsetHeight;

    widgetArrastando.style.left = newX + "px";
    widgetArrastando.style.top = newY + "px";

    // Atualiza as coordenadas em pixels reais do objeto
    widgetArrastando.properties.x = Math.round(newX);
    widgetArrastando.properties.y = Math.round(newY);

    if (typeof preencherTabelaAtual === "function") {
        preencherTabelaAtual();
    }
});

window.addEventListener("mouseup", () => {
    if (arrastando) {
        arrastando = false;
        widgetArrastando = null;
        if (typeof atualizarCodigoEditor === "function") {
            atualizarCodigoEditor();
        }
    }
});

function atualizarTamanhoCanvas() {
    const canvasEl = document.getElementById("canvas");
    if (canvasEl && window.interfaceProperties) {
        // Define o tamanho exato do canvas em pixels
        canvasEl.style.width = window.interfaceProperties.width + "px";
        canvasEl.style.height = window.interfaceProperties.height + "px";
        canvasEl.style.background = window.interfaceProperties.bg || "#121212";
    }
}
// Gerenciador de Seleção
function selecionarWidget(elemento) {
    deselecionarTodos();
    widgetSelecionado = elemento;
    window.widgetSelecionado = elemento; 
    elemento.classList.add("selected");
    
    if (typeof preencherTabelaAtual === "function") {
        preencherTabelaAtual();
    }
}

function deselecionarTodos() {
    document.querySelectorAll(".widget").forEach(w => w.classList.remove("selected"));
    widgetSelecionado = null;
    window.widgetSelecionado = null;
    if (typeof preencherTabelaAtual === "function") {
        preencherTabelaAtual();
    }
}

// Ação de Excluir Componente
document.getElementById("deleteWidget")?.addEventListener("click", () => {
    if (widgetSelecionado) {
        widgetSelecionado.remove();
        deselecionarTodos();
        if (typeof atualizarCodigoEditor === "function") {
            atualizarCodigoEditor();
        }
    }
});

window.criarWidget = criarWidget;
window.selecionarWidget = selecionarWidget;
window.deselecionarTodos = deselecionarTodos;