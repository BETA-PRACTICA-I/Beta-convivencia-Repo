const mainContent = document.getElementById('main-content');
const protocolTable = document.getElementById('protocol-table');
const protocoloSection = document.getElementById('protocolo-section');

const abrirBtn = document.getElementById('abrir-protocolo-btn');
const volverBtn = document.getElementById('volver-btn');
const btnAcoso = document.getElementById('btn-acoso');

if (abrirBtn && mainContent && protocolTable && protocoloSection) {
    abrirBtn.addEventListener('click', function() {
    mainContent.style.display = 'none';
    protocolTable.style.display = 'none';
    protocoloSection.style.display = 'block';
    });
}

if (volverBtn && mainContent && protocolTable && protocoloSection) {
    volverBtn.addEventListener('click', function() {
    mainContent.style.display = 'flex';
    protocolTable.style.display = 'table';
    protocoloSection.style.display = 'none';
    });
}
