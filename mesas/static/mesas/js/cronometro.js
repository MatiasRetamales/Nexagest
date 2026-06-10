/**
 * Gestiona los cronómetros de los pedidos de forma clara y profesional.
 */
function iniciarCronometros() {
    
    // 1. Buscamos todos los elementos que deben ser cronómetros
    const cronometros = document.querySelectorAll('.cronometro');

    cronometros.forEach(contenedor => {
        // Obtenemos la fecha de inicio desde el atributo data-desde que viene de Django
        const fechaInicio = new Date(contenedor.dataset.desde);
        const displayTiempo = contenedor.querySelector('.tiempo');

        function actualizarReloj() {
            // Calculamos la diferencia total en segundos
            const segundosTranscurridos = Math.floor((new Date() - fechaInicio) / 1000);

            // Extraemos horas, minutos y segundos
            const horas = Math.floor(segundosTranscurridos / 3600);
            const minutos = Math.floor((segundosTranscurridos % 3600) / 60);
            const segundos = segundosTranscurridos % 60;

            // Función interna para añadir el cero a la izquierda (ej: "05")
            const formatear = (num) => String(num).padStart(2, '0');

            // 2. Construimos el texto final (HH:MM:SS o solo MM:SS)
            let tiempoTexto = `${formatear(minutos)}:${formatear(segundos)}`;
            if (horas > 0) {
                tiempoTexto = `${formatear(horas)}:${tiempoTexto}`;
            }

            // 3. Actualizamos el HTML
            displayTiempo.textContent = tiempoTexto;

            // 4. Gestión de Urgencia: Si pasan más de 15 min (900 seg), se pone rojo
            const esUrgente = segundosTranscurridos > 900;
            contenedor.classList.toggle('cronometro--urgente', esUrgente);
        }

        // Ejecutamos de inmediato y luego cada segundo
        actualizarReloj();
        setInterval(actualizarReloj, 1000);
    });
}

// Esperamos a que el HTML esté listo para arrancar
document.addEventListener('DOMContentLoaded', iniciarCronometros);