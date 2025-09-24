const mainContent = document.getElementById('main-content');
const protocolTable = document.getElementById('protocol-table');
const protocoloSection = document.getElementById('protocolo-section');

const abrirBtn = document.getElementById('abrir-protocolo-btn');
const volverBtn = document.getElementById('volver-btn');

abrirBtn.addEventListener('click', function() {
    mainContent.style.display = 'none';
    protocolTable.style.display = 'none';
    protocoloSection.style.display = 'block';
});

volverBtn.addEventListener('click', function() {
    mainContent.style.display = 'flex';
    protocolTable.style.display = 'table';
    protocoloSection.style.display = 'none';
});