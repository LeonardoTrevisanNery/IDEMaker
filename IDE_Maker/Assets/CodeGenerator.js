// CodeGenerator.js - CORRIGIDO

function gerarCodigoPython(funcoesPersonalizadas = {}) {
    const comandos = new Set();
    
    document.querySelectorAll(".widget").forEach(widget => {
        const cmd = widget.properties.command;
        if (cmd && cmd.trim() !== "") {
            comandos.add(cmd.trim());
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
    
    codigo += `from BetterGuiSpark import GuiSpark

`;
    
    codigo += `gui = GuiSpark(
    title="${interfaceProperties.title}",
    width=${interfaceProperties.width},
    height=${interfaceProperties.height}
)

`;
    
    if (temaExistente && temaExistente !== "custom") {
        codigo += `gui.set_theme("${temaExistente}")

`;
    } else if (temaExistente === "custom" || (typeof temaAtual !== 'undefined' && temaAtual === "custom" && interfaceProperties.bg)) {
        const bg = interfaceProperties.bg || '#ffffff';
        const fg = interfaceProperties.fg || '#000000';
        const accent = (typeof customTheme !== 'undefined' && customTheme.accent) || '#af72fa';
        codigo += `gui.set_theme(
    theme_name="custom",
    bg="${bg}",
    fg="${fg}",
    accent="${accent}"
)

`;
    } else {
        codigo += `# gui.set_theme("dark")  # Descomente para ativar o tema escuro

`;
    }
    
    codigo += `# ===========================
# Funções
# ===========================

`;
    
    if (comandos.size === 0 && Object.keys(funcoesPersonalizadas).length === 0) {
        codigo += `# Nenhuma função definida
`;
    } else {
        comandos.forEach(cmd => {
            codigo += `def ${cmd}():`;
            
            if (funcoesPersonalizadas[cmd]) {
                const corpo = funcoesPersonalizadas[cmd];
                const linhas = corpo.split('\n');
                if (linhas.length === 0 || (linhas.length === 1 && linhas[0].trim() === '')) {
                    codigo += `
    pass
`;
                } else {
                    linhas.forEach(linha => {
                        if (linha.trim() !== '') {
                            codigo += '\n    ' + linha.trim();
                        }
                    });
                    codigo += '\n';
                }
            } else {
                codigo += `
    # Função ${cmd}
    pass
`;
            }
            
            codigo += '\n';
        });
        
        Object.keys(funcoesPersonalizadas).forEach(cmd => {
            if (!comandos.has(cmd)) {
                codigo += `def ${cmd}():`;
                const corpo = funcoesPersonalizadas[cmd];
                const linhas = corpo.split('\n');
                if (linhas.length === 0 || (linhas.length === 1 && linhas[0].trim() === '')) {
                    codigo += `
    pass
`;
                } else {
                    linhas.forEach(linha => {
                        if (linha.trim() !== '') {
                            codigo += '\n    ' + linha.trim();
                        }
                    });
                    codigo += '\n';
                }
                codigo += '\n';
            }
        });
    }
    
    codigo += `# ===========================
# Widgets
# ===========================

`;
    
    document.querySelectorAll(".widget").forEach(widget => {
        const p = widget.properties;
        const nome = p.name || gerarNomeWidget(widget.dataset.tipo);
        p.name = nome;
        
        let value = p.value;
        
        if (widget.dataset.tipo === "checkbox") {
            value = Boolean(value);
        } else if (widget.dataset.tipo === "slider" || widget.dataset.tipo === "progress") {
            value = Number(value || 0);
        } else if (value === "" || value === null) {
            value = "";
        }
        
        // ============================================
        // CORREÇÃO: items DEVE ser uma lista Python
        // ============================================
        let items = "None";
        if (Array.isArray(p.items) && p.items.length > 0) {
            // Já é um array - formata como lista Python
            const lista = p.items.map(item => `"${item}"`).join(", ");
            items = `[${lista}]`;
        } else if (typeof p.items === "string" && p.items.trim() !== "") {
            try {
                // Tenta parsear como JSON
                const parsed = JSON.parse(p.items);
                if (Array.isArray(parsed) && parsed.length > 0) {
                    const lista = parsed.map(item => `"${item}"`).join(", ");
                    items = `[${lista}]`;
                } else {
                    // Converte string separada por vírgula para lista
                    const lista = p.items.split(",").map(i => `"${i.trim()}"`).filter(i => i !== '""');
                    if (lista.length > 0) {
                        items = `[${lista.join(", ")}]`;
                    } else {
                        items = "None";
                    }
                }
            } catch {
                // Converte string separada por vírgula para lista
                const lista = p.items.split(",").map(i => `"${i.trim()}"`).filter(i => i !== '""');
                if (lista.length > 0) {
                    items = `[${lista.join(", ")}]`;
                } else {
                    items = "None";
                }
            }
        }
        
        let command = "None";
        if (p.command && p.command.trim() !== "") {
            command = p.command.trim();
        }
        
        let valorStr = JSON.stringify(value);
        if (widget.dataset.tipo === "checkbox") {
            valorStr = value ? "True" : "False";
        }
        
        codigo += `${nome} = gui.add_widget(
    "${widget.dataset.tipo}",
    x=${Number(p.x) || 0},
    y=${Number(p.y) || 0},
    width=${Number(p.width) || 100},
    height=${Number(p.height) || 30},
    text=${JSON.stringify(p.text || "")},
    bg=${JSON.stringify(p.bg || "")},
    fg=${JSON.stringify(p.fg || "")},
    hover_bg=${JSON.stringify(p.hover_bg || "")},
    pressed_bg=${JSON.stringify(p.pressed_bg || "")},
    border_radius=${Number(p.border_radius || 0)},
    command=${command},
    placeholder=${JSON.stringify(p.placeholder || "")},
    url=${JSON.stringify(p.url || "")},
    min_value=${Number(p.min_value || 0)},
    max_value=${Number(p.max_value || 100)},
    value=${valorStr},
    items=${items},
    orientation=${JSON.stringify(p.orientation || "horizontal")}
)

`;
    });
    
    codigo += `

gui.run()
`;
    
    return codigo;
}

window.gerarCodigoPython = gerarCodigoPython;