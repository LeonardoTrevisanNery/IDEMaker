// ============================================
// CODEGENERATOR.JS - IDE GENERATOR CORE
// ============================================

function gerarCodigoPython(funcoesPersonalizadas = {}) {
    const comandos = new Set();
    
    // Mapeia todos os comandos/funções declarados nos inputs dos elementos do canvas
    document.querySelectorAll(".widget").forEach(widget => {
        if (widget.properties && widget.properties.command) {
            const cmd = widget.properties.command.trim();
            if (cmd !== "") {
                comandos.add(cmd);
            }
        }
    });
    
    const editor = document.getElementById("codigoEditor");
    let temaExistente = null;
    
    if (editor && editor.value) {
        const temaMatch = editor.value.match(/gui\.set_theme\s*\(\s*["']([^"']+)["']\s*\)/);
        if (temaMatch) {
            temaExistente = temaMatch[1];
        }
    }
    
    if (!temaExistente && typeof temaAtual !== 'undefined' && temaAtual) {
        temaExistente = temaAtual;
    }
    
    let codigo = "";
    
    // Imports da biblioteca Spark
    codigo += `from Assets.Core.Base import GuiSpark\n\n`;
    
    // Inicialização da Janela com dados dinâmicos do painel
    const title = window.interfaceProperties?.title || "Nova Interface";
    const width = window.interfaceProperties?.width || 900;
    const height = window.interfaceProperties?.height || 650;
    
    codigo += `gui = GuiSpark(\n    title="${title}",\n    width=${width},\n    height=${height}\n)\n\n`;
    
    // Injeção de tema se configurado
    if (temaExistente) {
        codigo += `gui.set_theme("${temaExistente}")\n\n`;
    }
    
    // ============================================
    // SEÇÃO DE FUNÇÕES / EVENTOS
    // ============================================
    codigo += `# ===========================\n`;
    codigo += `# Funções de Eventos\n`;
    codigo += `# ===========================\n`;
    
    if (comandos.size === 0) {
        codigo += `# Nenhuma função de evento vinculada aos componentes.\n`;
    } else {
        comandos.forEach(cmd => {
            codigo += `def ${cmd}():\n`;
            if (funcoesPersonalizadas[cmd]) {
                // Se a função já existia no código anterior, preserva o escopo interno dela
                let bloco = funcoesPersonalizadas[cmd].trim();
                if (bloco === "" || bloco === "pass") {
                    codigo += `    print("Botão executou a ação: ${cmd}")\n`;
                } else {
                    // Garante a indentação de 4 espaços para o bloco Python
                    codigo += bloco.split('\n').map(linha => linha.startsWith("    ") ? linha : "    " + linha).join('\n') + "\n";
                }
            } else {
                // Caso seja uma nova ação, cria um template padrão print funcional
                codigo += `    print("Ação acionada: ${cmd}")\n`;
            }
            codigo += `\n`;
        });
    }
    
    // ============================================
    // SEÇÃO DE COMPONENTES (WIDGETS)
    // ============================================
    codigo += `# ===========================\n`;
    codigo += `# Definição dos Componentes Visuais\n`;
    codigo += `# ===========================\n`;
    
    const widgets = document.querySelectorAll(".widget");
    if (widgets.length === 0) {
        codigo += `# Arraste elementos da paleta esquerda para renderizar código aqui\n`;
    } else {
        widgets.forEach(widget => {
            const p = widget.properties || {};
            const nome = widget.id;
            const tipo = widget.dataset.tipo;
            
            let commandStr = "None";
            if (p.command && p.command.trim() !== "") {
                commandStr = p.command.trim();
            }
            
            let itemsStr = "None";
            if (p.items && p.items.trim() !== "") {
                const lista = p.items.split(',').map(i => `'${i.trim()}'`);
                itemsStr = `[${lista.join(", ")}]`;
            }

            // Estrutura padrão de geração limpa por linha do componente
            codigo += `${nome} = gui.add_widget(\n`;
            codigo += `    "${tipo}",\n`;
            codigo += `    x=${Number(p.x) || 0},\n`;
            codigo += `    y=${Number(p.y) || 0},\n`;
            codigo += `    width=${Number(p.width) || 100},\n`;
            codigo += `    height=${Number(p.height) || 30},\n`;
            codigo += `    text=${JSON.stringify(p.text || "")},\n`;
            codigo += `    bg=${JSON.stringify(p.bg || "")},\n`;
            codigo += `    fg=${JSON.stringify(p.fg || "")},\n`;
            codigo += `    command=${commandStr},\n`;
            codigo += `    items=${itemsStr}\n`;
            codigo += `)\n\n`;
        });
    }
    
    // Finalizador da aplicação Spark
    codigo += `gui.run()\n`;
    
    return codigo;
}

// Exporta a função para o motor central da IDE
window.gerarCodigoPython = gerarCodigoPython;