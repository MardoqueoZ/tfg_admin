var dataTableReco; // Variable global para almacenar la instancia de DataTable

$(document).ready(function() {
    initDataTable(); // Inicializar DataTable al cargar la página
});

function initDataTable() {
    if (dataTableReco) {
        dataTableReco.destroy(); // Destruir la instancia anterior si existe
    }

    dataTableNoticias = $('#datatable-recomendaciones').DataTable({
        'lengthMenu': [5, 10, 25],
        language: {
            url: '//cdn.datatables.net/plug-ins/2.0.5/i18n/es-ES.json',
        },
        'processing': true,
        responsive: true,
        'columnDefs': [
            { 'className': 'dt-center', 'targets': '_all' } // Centrar el texto en todas las columnas
        ]
    });
}

