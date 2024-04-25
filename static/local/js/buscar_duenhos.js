let error = document.getElementById('error');
let cedula = document.getElementById('ci');
let btnBuscar = document.getElementById('buscar');
let mensaje = document.createElement('span');
let btnRecargar = document.getElementById('recargar');

btnBuscar.addEventListener('click', () => {
    event.preventDefault(); // Detener la propagación del evento click
    cedula = cedula.value;
    if (cedula === '') {
        error.appendChild(mensaje);
        mensaje.innerHTML = 'El campo no puede estar vacío';
        mensaje.style.color = 'red';
    } else {
        // Envíar el formulario si la cédula no está vacía
        document.getElementById('buscarDuenho').submit();
    }
});

    