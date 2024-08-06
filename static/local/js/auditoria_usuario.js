var dataTableAuUsuarios;

$(document).ready(function() {
    initDataTable();
});

function initDataTable() {
    if (dataTableAuUsuarios) {
        dataTableAuUsuarios.destroy();
    }

    dataTableAuUsuarios = $('#datatable_au_usuarios').DataTable({
        'lengthMenu': [5, 10, 25],
        language: {
            url: 'https://cdn.datatables.net/plug-ins/2.0.7/i18n/es-MX.json',
        },
        'processing': true,
        responsive: true,
        'columnDefs': [
            { 'className': 'dt-center', 'targets': '_all' } // Centrar el texto en todas las columnas
        ]
    });
}