// ========================================
// ELEMENTOS
// ========================================

const estadoIcono =
    document.getElementById(
        'estado-icono'
    );

const estadoTitulo =
    document.getElementById(
        'estado-titulo'
    );

const estadoDescripcion =
    document.getElementById(
        'estado-descripcion'
    );


const pasoRecibido =
    document.getElementById(
        'paso-recibido'
    );

const pasoPreparando =
    document.getElementById(
        'paso-preparando'
    );

const pasoListo =
    document.getElementById(
        'paso-listo'
    );

const pasoEnCamino =
    document.getElementById(
        'paso-en-camino'
    );


// ========================================
// ACTUALIZAR ESTADO
// ========================================

function actualizarEstado() {

    fetch(
        window.location.href,
        {
            headers: {
                'X-Requested-With':
                    'XMLHttpRequest'
            }
        }
    )

    .then(response => {

        if (!response.ok) {

            throw new Error(
                'Error al consultar el pedido.'
            );

        }

        return response.json();

    })

    .then(data => {

        console.log(
            'Estado del pedido:',
            data.estado
        );


        // ========================================
        // PEDIDO RECIBIDO
        // ========================================

        if (
            data.estado === 'pendiente'
        ) {

            estadoIcono.textContent =
                '🟡';

            estadoTitulo.textContent =
                'Pedido recibido';

            estadoDescripcion.textContent =
                'El restaurante está revisando tu pedido.';


            pasoRecibido.classList.add(
                'activo'
            );

            pasoPreparando.classList.remove(
                'activo'
            );

            pasoListo.classList.remove(
                'activo'
            );

            if (pasoEnCamino) {

                pasoEnCamino.classList.remove(
                    'activo'
                );

            }

        }


        // ========================================
        // EN PREPARACIÓN
        // ========================================

        else if (
            data.estado === 'en_preparacion'
        ) {

            estadoIcono.textContent =
                '👨‍🍳';

            estadoTitulo.textContent =
                'Preparando tu pedido';

            estadoDescripcion.textContent =
                'Tu pedido ya está siendo preparado.';


            pasoRecibido.classList.add(
                'activo'
            );

            pasoPreparando.classList.add(
                'activo'
            );

            pasoListo.classList.remove(
                'activo'
            );

            if (pasoEnCamino) {

                pasoEnCamino.classList.remove(
                    'activo'
                );

            }

        }


        // ========================================
        // LISTO
        // ========================================

        else if (
            data.estado === 'listo'
        ) {

            estadoIcono.textContent =
                '🟢';

            estadoTitulo.textContent =
                '¡Tu pedido está listo!';


            if (
                data.tipo_entrega === 'retiro'
            ) {

                estadoDescripcion.textContent =
                    'Puedes retirarlo en el local.';

            } else {

                estadoDescripcion.textContent =
                    'Tu pedido está listo para ser entregado.';

            }


            pasoRecibido.classList.add(
                'activo'
            );

            pasoPreparando.classList.add(
                'activo'
            );

            pasoListo.classList.add(
                'activo'
            );

            if (pasoEnCamino) {

                pasoEnCamino.classList.remove(
                    'activo'
                );

            }

        }


        // ========================================
        // EN CAMINO
        // ========================================

        else if (
            data.estado === 'en_camino'
        ) {

            estadoIcono.textContent =
                '🚗';

            estadoTitulo.textContent =
                '¡Tu pedido va en camino!';

            estadoDescripcion.textContent =
                'El repartidor ya salió con tu pedido.';


            pasoRecibido.classList.add(
                'activo'
            );

            pasoPreparando.classList.add(
                'activo'
            );

            pasoListo.classList.add(
                'activo'
            );

            if (pasoEnCamino) {

                pasoEnCamino.classList.add(
                    'activo'
                );

            }

        }


        // ========================================
        // ENTREGADO
        // ========================================

        else if (
            data.estado === 'entregado'
        ) {

            estadoIcono.textContent =
                '✅';

            estadoTitulo.textContent =
                'Pedido entregado';

            estadoDescripcion.textContent =
                '¡Gracias por tu compra!';


            pasoRecibido.classList.add(
                'activo'
            );

            pasoPreparando.classList.add(
                'activo'
            );

            pasoListo.classList.add(
                'activo'
            );

            if (pasoEnCamino) {

                if (
                    data.tipo_entrega === 'delivery'
                ) {

                    pasoEnCamino.classList.add(
                        'activo'
                    );

                }

            }


            // Dejar de consultar

            clearInterval(
                intervaloEstado
            );

        }


        // ========================================
        // CANCELADO
        // ========================================

        else if (
            data.estado === 'cancelado'
        ) {

            estadoIcono.textContent =
                '❌';

            estadoTitulo.textContent =
                'Pedido cancelado';

            estadoDescripcion.textContent =
                'Este pedido fue cancelado por el restaurante.';


            clearInterval(
                intervaloEstado
            );

        }

    })

    .catch(error => {

        console.error(
            'Error actualizando estado:',
            error
        );

    });

}


// ========================================
// CONSULTAR CADA 5 SEGUNDOS
// ========================================

const intervaloEstado =
    setInterval(
        actualizarEstado,
        5000
    );


// ========================================
// CONSULTAR INMEDIATAMENTE
// ========================================

actualizarEstado();