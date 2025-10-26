document.addEventListener('DOMContentLoaded', function () {
    const mainContent = document.getElementById('main-content');
    const protocolTable = document.getElementById('protocol-table');
    const protocoloSection = document.getElementById('protocolo-section');

    const abrirBtn = document.getElementById('abrir-protocolo-btn');
    const volverBtn = document.getElementById('volver-btn');

    // Mostrar / ocultar sección de inicio de protocolo (mantener lógica previa)
    if (abrirBtn && mainContent && protocolTable && protocoloSection) {
        abrirBtn.addEventListener('click', function () {
            mainContent.style.display = 'none';
            protocolTable.style.display = 'none';
            protocoloSection.style.display = 'block';
        });
    }

    if (volverBtn && mainContent && protocolTable && protocoloSection) {
        volverBtn.addEventListener('click', function () {
            mainContent.style.display = 'flex';
            protocolTable.style.display = 'table';
            protocoloSection.style.display = 'none';
        });
    }

    // --- Lógica para fila expandible (panel de acciones) ---
    if (!protocolTable) return;

    let openRowId = null;

    function createExpandedRow(protocoloId) {
        const tr = document.createElement('tr');
        tr.className = 'protocol-expanded';
        tr.dataset.for = protocoloId;

        const td = document.createElement('td');
        td.colSpan = 8;
        td.innerHTML = `
            <div class="expanded-panel" role="region" aria-label="Acciones protocolo ${protocoloId}">
                <div>
                    <strong>Acciones para protocolo #${protocoloId}</strong>
                    <p style="margin:6px 0 0;color:#555;">Selecciona una acción. (UI nomás xd)</p>
                </div>
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="expanded-actions">
                        <a href="#" class="btn-ver" data-id="${protocoloId}">Ver</a>
                        <a href="#" class="btn-editar" data-id="${protocoloId}">Editar</a>
                        <a href="#" class="btn-descargar" data-id="${protocoloId}">Descargar</a>
                    </div>
                    <button class="expanded-close" aria-label="Cerrar panel" title="Cerrar">✕</button>
                </div>
            </div>
        `;
        tr.appendChild(td);
        return tr;
    }

    // Ignorar clicks que vienen desde el menú de estado u otros controles dentro de la fila
    function clickFromEstado(target) {
        return !!target.closest('.estado-dropdown');
    }

    // Delegación: clic en tbody
    const tbody = protocolTable.querySelector('tbody');
    if (!tbody) return;

    tbody.addEventListener('click', function (evt) {
        const target = evt.target;

        // Si el click proviene del menú de estado, enlaces o botones dentro de la fila, no togglear el panel
        if (clickFromEstado(target) || target.closest('a') || target.closest('button.estado-btn')) {
            return;
        }

        const row = target.closest('tr.protocol-row');
        if (!row) return;
        const protocoloId = String(row.dataset.protocoloId);

        // Cerrar panel abierto distinto
        if (openRowId && openRowId !== protocoloId) {
            const existing = protocolTable.querySelector(`tr.protocol-expanded[data-for="${openRowId}"]`);
            if (existing) existing.remove();
            openRowId = null;
        }

        // Toggle: si ya existe, eliminar; si no, crear
        const existingForThis = protocolTable.querySelector(`tr.protocol-expanded[data-for="${protocoloId}"]`);
        if (existingForThis) {
            existingForThis.remove();
            openRowId = null;
            return;
        }

        const expandedRow = createExpandedRow(protocoloId);
        row.parentNode.insertBefore(expandedRow, row.nextSibling);
        openRowId = protocoloId;

        // Cerrar con X
        const closeBtn = expandedRow.querySelector('.expanded-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                expandedRow.remove();
                openRowId = null;
            });
        }

        // Evitar navegación en los links por ahora y loguear acción
        expandedRow.querySelectorAll('.expanded-actions a').forEach(a => {
            a.addEventListener('click', function (e) {
                e.preventDefault();
                console.log(`${this.textContent.trim()} pedido para protocolo ${this.dataset.id}`);
            });
        });
    });

    // Click fuera del área: cierra panel abierto
    document.addEventListener('click', function (e) {
        const expanded = protocolTable.querySelector('tr.protocol-expanded');
        if (!expanded) return;
        if (!e.target.closest('tr.protocol-row') && !e.target.closest('tr.protocol-expanded')) {
            expanded.remove();
            openRowId = null;
        }
    });

    // Tecla ESC cierra panel si está abierto
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            const expanded = protocolTable.querySelector('tr.protocol-expanded');
            if (expanded) {
                expanded.remove();
                openRowId = null;
            }
        }
    });
});
