    function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Esta cookie se llama 'csrftoken'
            if (cookie.substring(0, 10) === ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

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

        // --- Lógica 1: Click en el BOTÓN de Estado ---
        const estadoBtn = target.closest('.estado-btn');
        if (estadoBtn) {
            evt.stopPropagation(); // ¡Importante! Detenemos el click AQUI
            
            const dropdown = estadoBtn.closest('.estado-dropdown');
            const isOpen = dropdown.classList.contains('active');

            // Cerramos todos los OTROS dropdowns que puedan estar abiertos
            document.querySelectorAll('.estado-dropdown.active').forEach(d => {
                if (d !== dropdown) {
                    d.classList.remove('active');
                    d.querySelector('.estado-opciones').setAttribute('aria-hidden', 'true');
                }
            });

            // Abrimos/cerramos el dropdown actual
            dropdown.classList.toggle('active');
            dropdown.querySelector('.estado-opciones').setAttribute('aria-hidden', !isOpen);
            
            return; // ¡Salimos! No queremos expandir la fila
        }
        
        // --- Lógica 2: Click en una OPCIÓN de Estado ---
        // --- Lógica 2: Click en una OPCIÓN de Estado (¡CON FETCH/AJAX!) ---
        const estadoOpcion = target.closest('.estado-opciones a');
        if (estadoOpcion) {
            evt.stopPropagation(); // ¡Importante! Detenemos el click AQUI
            
            const dropdown = estadoOpcion.closest('.estado-dropdown');
            const nuevoEstado = estadoOpcion.dataset.value;
            const protocoloId = dropdown.closest('tr.protocol-row').dataset.protocoloId;
            const csrfToken = getCSRFToken(); // 1. Obtenemos el token de seguridad
            
            // Feedback visual: Mostramos "Guardando..."
            const textoBoton = dropdown.querySelector('.estado-texto');
            const textoOriginal = textoBoton.textContent;
            textoBoton.textContent = 'Guardando...';

            // 2. ¡Aquí empieza la magia de fetch!
            fetch('/protocolos/actualizar-estado/', { // ¡La URL que creamos en urls.py!
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // 3. Enviamos el token en la cabecera
                },
                body: JSON.stringify({ // 4. Enviamos los datos como JSON
                    'protocolo_id': protocoloId,
                    'nuevo_estado': nuevoEstado
                })
            })
            .then(response => {
                // Convertimos la respuesta de Django (que es JSON)
                if (!response.ok) {
                    // Si Django da un error (403, 404, 500...), lo lanzamos
                    throw new Error(`Error del servidor: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // 5. Leemos la respuesta de nuestra vista en views.py
                if (data.status === 'success') {
                    // ¡Éxito! Actualizamos el texto final
                    textoBoton.textContent = nuevoEstado;
                    console.log(`Éxito: ${data.message}`);
                } else {
                    // Si la vista nos da un error (ej: "No tienes permisos")
                    alert(`Error: ${data.message}`);
                    textoBoton.textContent = textoOriginal; // Revertimos el texto
                }
            })
            .catch(error => {
                // Si hay un error de red (ej: el servidor se cayó o la URL está mal)
                console.error('Error en fetch:', error);
                alert('Error de red. No se pudo actualizar el estado.');
                textoBoton.textContent = textoOriginal; // Revertimos el texto
            })
            .finally(() => {
                // 6. En cualquier caso (éxito o error), cerramos el menú
                dropdown.classList.remove('active');
                dropdown.querySelector('.estado-opciones').setAttribute('aria-hidden', 'true');
            });
            
            return; // ¡Salimos! No queremos expandir la fila
        }

        // --- Lógica 3: Click en la FILA (para expandir) ---
        
        // Ignoramos si el click fue en un link (ej: los de Ver, Editar, etc. del panel)
        if (target.closest('a')) {
            return;
        }

        const row = target.closest('tr.protocol-row');
        if (!row) return; // Click fue en el espacio vacío del tbody
        
        const protocoloId = String(row.dataset.protocoloId);

        // Lógica original para cerrar otros paneles
        if (openRowId && openRowId !== protocoloId) {
            const existing = protocolTable.querySelector(`tr.protocol-expanded[data-for="${openRowId}"]`);
            if (existing) existing.remove();
        }

        // Lógica original para cerrar el panel actual si ya estaba abierto
        const existingForThis = protocolTable.querySelector(`tr.protocol-expanded[data-for="${protocoloId}"]`);
        if (existingForThis) {
            existingForThis.remove();
            openRowId = null;
            return;
        }

        // Lógica original para crear y mostrar el panel
        const expandedRow = createExpandedRow(protocoloId, row);
        row.parentNode.insertBefore(expandedRow, row.nextSibling);
        openRowId = protocoloId;

        // Lógica original para el botón de cerrar (X) del panel
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