// Assets/SideNumbers.js

document.addEventListener("DOMContentLoaded", () => {
    const editor = document.getElementById("codigoEditor");
    const lineCounter = document.getElementById("lineNumbers");

    if (!editor || !lineCounter) {
        console.warn("[SideNumbers] Elementos do editor de texto não encontrados.");
        return;
    }

    /**
     * Atualiza a quantidade de números de linha baseada nas quebras de linha (\n)
     */
    function updateLineNumbers() {
        // Divide o texto pelas quebras de linha para contar as linhas
        const lines = editor.value.split("\n");
        const lineCount = lines.length;

        // Gera a string de números pulando linha por linha
        let linesHTML = "";
        for (let i = 1; i <= lineCount; i++) {
            linesHTML += i + "<br>";
        }

        lineCounter.innerHTML = linesHTML;
    }

    /**
     * Sincroniza a rolagem vertical do contador com a do editor de código
     */
    function syncScroll() {
        lineCounter.scrollTop = editor.scrollTop;
    }

    // --- EVENTOS DO EDITOR ---

    // Atualiza ao digitar ou modificar o texto
    editor.addEventListener("input", updateLineNumbers);

    // Sincroniza o scroll do contador ao rolar o editor
    editor.addEventListener("scroll", syncScroll);

    // Captura ações extras como colagens, cortes ou desfazer (Undo)
    editor.addEventListener("cut", () => setTimeout(updateLineNumbers, 10));
    editor.addEventListener("paste", () => setTimeout(updateLineNumbers, 10));
    editor.addEventListener("keydown", (e) => {
        // Atualização rápida para teclas que modificam o número de linhas (Enter, Backspace, Delete)
        if (e.key === "Enter" || e.key === "Backspace" || e.key === "Delete") {
            setTimeout(updateLineNumbers, 10);
        }
    });

    // Executa uma carga inicial para caso o editor já abra com algum código carregado
    updateLineNumbers();
});