document.addEventListener('DOMContentLoaded', function () {
    const mainContent = document.getElementById('main-content');
    const protocolTable = document.getElementById('protocol-table');
    const protocoloSection = document.getElementById('protocolo-section');

    const abrirBtn = document.getElementById('abrir-protocolo-btn');
    const volverBtn = document.getElementById('volver-btn');

    // Mostrar / ocultar sección de inicio de protocolo
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

    // FUNCIÓN CORREGIDA: Acepta 'row' para leer las URLs
    function createExpandedRow(protocoloId, row) {
        // Leemos las URLs desde los data attributes de la fila
        const urlVer = row.dataset.urlVer;
        const urlDescargar = row.dataset.urlDescargar;

        const tr = document.createElement('tr');
        tr.className = 'protocol-expanded';
        tr.dataset.for = protocoloId;

        const td = document.createElement('td');
        td.colSpan = 8;
        // Usamos las variables con las URLs correctas que leímos
        td.innerHTML = `
            <div class="expanded-panel" role="region" aria-label="Acciones protocolo ${protocoloId}">
                <div>
                    <strong>Acciones para protocolo #${protocoloId}</strong>
                    <p style="margin:6px 0 0;color:#555;">Selecciona una acción.</p>
                </div>
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="expanded-actions">
                        <a href="${urlVer}" class="btn-ver" data-id="${protocoloId}">Ver</a>
                        <a href="/protocolos/editar/paso1/${protocoloId}/" class="btn-editar" data-id="${protocoloId}">Editar</a>
                        <a href="${urlDescargar}" class="btn-descargar" data-id="${protocoloId}">Descargar</a>
                    </div>
                    <button class="expanded-close" aria-label="Cerrar panel" title="Cerrar">✕</button>
                </div>
            </div>
        `;
        tr.appendChild(td);
        return tr;
    }

    // Función auxiliar para ignorar clicks en el menú de estado
    function clickFromEstado(target) {
        return !!target.closest('.estado-dropdown');
    }

    const tbody = protocolTable.querySelector('tbody');
    if (!tbody) return;

    // BLOQUE CORREGIDO: Maneja los clicks en la tabla
    tbody.addEventListener('click', function (evt) {
        const target = evt.target;

        if (clickFromEstado(target) || target.closest('a') || target.closest('button.estado-btn')) {
            return;
        }

        const row = target.closest('tr.protocol-row');
        if (!row) return;
        const protocoloId = String(row.dataset.protocoloId);

        if (openRowId && openRowId !== protocoloId) {
            const existing = protocolTable.querySelector(`tr.protocol-expanded[data-for="${openRowId}"]`);
            if (existing) existing.remove();
        }

        const existingForThis = protocolTable.querySelector(`tr.protocol-expanded[data-for="${protocoloId}"]`);
        if (existingForThis) {
            existingForThis.remove();
            openRowId = null;
            return;
        }

        // ¡Aquí está la magia! Le pasamos la 'row' a la función
        const expandedRow = createExpandedRow(protocoloId, row);
        row.parentNode.insertBefore(expandedRow, row.nextSibling);
        openRowId = protocoloId;

        const closeBtn = expandedRow.querySelector('.expanded-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                expandedRow.remove();
                openRowId = null;
            });
        }
    });

    // Cierra el panel si se hace click fuera de la tabla
    document.addEventListener('click', function (e) {
        if (openRowId && !e.target.closest('.protocol-table')) {
            const expanded = protocolTable.querySelector(`tr.protocol-expanded[data-for="${openRowId}"]`);
            if (expanded) {
                expanded.remove();
                openRowId = null;
            }
        }
    });

    // Cierra el panel con la tecla ESC
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && openRowId) {
            const expanded = protocolTable.querySelector(`tr.protocol-expanded[data-for="${openRowId}"]`);
            if (expanded) {
                expanded.remove();
                openRowId = null;
            }
        }
    });
});