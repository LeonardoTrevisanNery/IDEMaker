// ============================================
// LOCK.JS - Sistema Anti-Duplicação Definitivo
// ============================================

class CodeLock {
    constructor() {
        this.locked = false;
        this.modified = false;
        this.originalCode = '';
        this.currentCode = '';
        this.lockReason = '';
        this.isParsing = false;
        this.isGenerating = false;
        this.parseCount = 0;
        this.lastParseTime = 0;
        this.codeCache = '';
    }

    lock(reason = 'Edição manual') {
        this.locked = true;
        this.lockReason = reason;
        this.modified = true;
        
        const editor = document.getElementById('codigoEditor');
        if (editor) {
            this.originalCode = editor.value;
            this.currentCode = editor.value;
            this.codeCache = editor.value;
        }
        
        console.log(`🔒 Código BLOQUEADO: ${reason}`);
        this._updateUI();
        return true;
    }

    unlock() {
        this.locked = false;
        this.modified = false;
        this.lockReason = '';
        console.log('🔓 Código DESBLOQUEADO');
        this._updateUI();
        return true;
    }

    canOverwrite() {
        if (this.locked) {
            console.warn(`⚠️ Sobrescrita negada: ${this.lockReason}`);
            return false;
        }
        return true;
    }

    detectManualEdit() {
        const editor = document.getElementById('codigoEditor');
        if (!editor) return;

        if (editor.value !== this.codeCache) {
            this.lock('Alteração manual detectada');
            this.codeCache = editor.value;
        }
    }

    syncEditor() {
        const editor = document.getElementById('codigoEditor');
        if (editor) {
            this.currentCode = editor.value;
        }
    }

    _updateUI() {
        const indicator = document.getElementById('lockIndicator');
        if (indicator) {
            indicator.style.display = this.locked ? 'inline' : 'none';
            indicator.title = this.lockReason;
        }
    }

    getStatus() {
        return {
            locked: this.locked,
            modified: this.modified,
            reason: this.lockReason,
            isParsing: this.isParsing,
            isGenerating: this.isGenerating,
            originalCodeLength: this.originalCode.length,
            currentCodeLength: this.currentCode.length,
            cacheLength: this.codeCache.length
        };
    }
}

const codeLock = new CodeLock();

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔒 CodeLock Anti-Loop com Cache carregado');
    
    const editor = document.getElementById('codigoEditor');
    if (editor) {
        editor.addEventListener('focus', function() {
            this._usuarioDigitando = true;
            codeLock.detectManualEdit();
        });
        
        editor.addEventListener('input', function() {
            this._usuarioDigitando = true;
            codeLock.detectManualEdit();
            codeLock.syncEditor();
        });
        
        editor.addEventListener('blur', function() {
            this._usuarioDigitando = false;
            codeLock.syncEditor();
        });
        
        editor.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.shiftKey && e.key === 'L') {
                e.preventDefault();
                if (codeLock.locked) {
                    codeLock.unlock();
                } else {
                    codeLock.lock('Bloqueado manualmente');
                }
            }
        });
    }
});

window.codeLock = codeLock;