var dataTableNoticias; // Variable global para almacenar la instancia de DataTable

$(document).ready(function() {
    initDataTable(); // Inicializar DataTable al cargar la página
});

function initDataTable() {
    if (dataTableNoticias) {
        dataTableNoticias.destroy(); // Destruir la instancia anterior si existe
    }

    dataTableNoticias = $('#datatable-noticias').DataTable({
        'lengthMenu': [5, 10, 25],
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.0.7/i18n/es-MX.json',
        },
        'responsive': true,
        'processing': true,
        'columnDefs': [
            { 'className': 'dt-center', 'targets': '_all' } // Centrar el texto en todas las columnas
        ]
    });
}

