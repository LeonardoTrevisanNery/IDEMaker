// --- SISTEMA DE ZOOM DO CANVAS ---

// Variáveis de controle de escala
let canvasScale = 1.0;
const SCALE_STEP = 0.1; // Ajuste de 10% por clique
const MIN_SCALE = 0.4;  // Zoom mínimo (40%)
const MAX_SCALE = 2.5;  // Zoom máximo (250%)

// Inicializa propriedades visuais necessárias no canvas para um zoom suave
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('canvas');
    if (canvas) {
        canvas.style.transition = "transform 0.15s ease-out"; // Transição suave
        canvas.style.transformOrigin = "center center";       // Origem do zoom no centro
    }
});

/**
 * Aplica a escala atual ao elemento canvas e notifica o console da IDE.
 */
function aplicarZoom() {
    const canvas = document.getElementById('canvas');
    if (!canvas) return;

    canvas.style.transform = `scale(${canvasScale})`;
    
    // Atualiza o console da sua IDE com a porcentagem atual
    const porcentagem = Math.round(canvasScale * 100);
    logNoConsole(`Zoom ajustado para: ${porcentagem}%`);
}

/**
 * Aumenta o zoom (Zoom In)
 */
function canvazoomin() {
    if (canvasScale < MAX_SCALE) {
        // O use de .toFixed(1) evita bugs de precisão de ponto flutuante do JS (ex: 1.1000000000000001)
        canvasScale = parseFloat((canvasScale + SCALE_STEP).toFixed(1));
        aplicarZoom();
    } else {
        logNoConsole("⚠️ Limite máximo de zoom atingido (250%)");
    }
}

/**
 * Diminui o zoom (Zoom Out)
 */
function canvazoomout() {
    if (canvasScale > MIN_SCALE) {
        canvasScale = parseFloat((canvasScale - SCALE_STEP).toFixed(1));
        aplicarZoom();
    } else {
        logNoConsole("⚠️ Limite mínimo de zoom atingido (40%)");
    }
}

/**
 * Função auxiliar para enviar mensagens ao console da sua interface
 */
function logNoConsole(mensagem) {
    const consoleOutput = document.getElementById('consoleOutput');
    if (consoleOutput) {
        consoleOutput.textContent += `[SparkDesigner] ${mensagem}\n`;
        consoleOutput.scrollTop = consoleOutput.scrollHeight; // Auto-scroll para o final
    }
}