const LIMITE_AMARILLO = 15 * 60; // 15 min en segundos
const LIMITE_ROJO     = 25 * 60; // 25 min en segundos

function actualizarPrioridad(el, diff) {
    el.classList.remove('prioridad-verde', 'prioridad-amarillo', 'prioridad-rojo');

    if (diff >= LIMITE_ROJO) {
        el.classList.add('prioridad-rojo');
    } else if (diff >= LIMITE_AMARILLO) {
        el.classList.add('prioridad-amarillo');
    } else {
        el.classList.add('prioridad-verde');
    }
}

function iniciarCronometrosCocina() {
    document.querySelectorAll('.pedido[data-desde]').forEach(el => {
        const desde = new Date(el.dataset.desde);
        const spanTiempo = el.querySelector('.tiempo');

        function actualizar() {
            const diff = Math.floor((new Date() - desde) / 1000);

            const horas    = Math.floor(diff / 3600);
            const minutos  = Math.floor((diff % 3600) / 60);
            const segundos = diff % 60;
            const pad = n => String(n).padStart(2, '0');

            spanTiempo.textContent = horas > 0
                ? `${pad(horas)}:${pad(minutos)}:${pad(segundos)}`
                : `${pad(minutos)}:${pad(segundos)}`;

            actualizarPrioridad(el, diff);
        }

        actualizar();
        setInterval(actualizar, 1000);
    });
}

document.addEventListener('DOMContentLoaded', iniciarCronometrosCocina);