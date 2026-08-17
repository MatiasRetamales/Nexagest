let carrito = [];


// ========================================
// AGREGAR PRODUCTOS
// ========================================

const botonesAgregar =
    document.querySelectorAll('.btn-agregar');

botonesAgregar.forEach(boton => {

    boton.addEventListener('click', () => {

        const id =
            boton.dataset.id;

        const nombre =
            boton.dataset.nombre;

        const precio =
            Number(boton.dataset.precio);


        const productoExistente =
            carrito.find(
                producto => producto.id === id
            );


        if (productoExistente) {

            productoExistente.cantidad += 1;

        } else {

            carrito.push({

                id: id,

                nombre: nombre,

                precio: precio,

                cantidad: 1

            });

        }


        actualizarCarrito();

    });

});


// ========================================
// ACTUALIZAR CARRITO
// ========================================

function actualizarCarrito() {

    let cantidadTotal = 0;

    let precioTotal = 0;


    carrito.forEach(producto => {

        cantidadTotal += producto.cantidad;

        precioTotal +=
            producto.precio *
            producto.cantidad;

    });


    document.getElementById(
        'cantidad-carrito'
    ).textContent =
        `${cantidadTotal} productos`;


    document.getElementById(
        'total-carrito'
    ).textContent =
        `$${precioTotal.toLocaleString('es-CL')}`;

}


// ========================================
// ELEMENTOS DEL PEDIDO
// ========================================

const btnCarrito =
    document.getElementById(
        'btn-carrito'
    );


const resumenPedido =
    document.getElementById(
        'resumen-pedido'
    );


const cerrarPedido =
    document.getElementById(
        'cerrar-pedido'
    );


const listaPedido =
    document.getElementById(
        'lista-pedido'
    );


const totalPedido =
    document.getElementById(
        'total-pedido'
    );


// ========================================
// ABRIR RESUMEN DEL PEDIDO
// ========================================

btnCarrito.addEventListener(
    'click',
    () => {

        listaPedido.innerHTML = '';

        let total = 0;


        carrito.forEach(producto => {

            const subtotal =
                producto.precio *
                producto.cantidad;


            total += subtotal;


            listaPedido.innerHTML += `

                <div class="item-pedido">

                    <div class="item-pedido-info">

                        <strong>
                            ${producto.nombre}
                        </strong>

                        <span>
                            ${producto.cantidad} x
                            $${producto.precio.toLocaleString('es-CL')}
                        </span>

                    </div>


                    <strong>
                        $${subtotal.toLocaleString('es-CL')}
                    </strong>

                </div>

            `;

        });


        totalPedido.textContent =
            `$${total.toLocaleString('es-CL')}`;


        resumenPedido.classList.remove(
            'oculto'
        );

    }
);


// ========================================
// CERRAR RESUMEN
// ========================================

cerrarPedido.addEventListener(
    'click',
    () => {

        resumenPedido.classList.add(
            'oculto'
        );

    }
);


// ========================================
// FORMULARIO DEL CLIENTE
// ========================================

const btnContinuar =
    document.getElementById(
        'btn-continuar'
    );


const datosCliente =
    document.getElementById(
        'datos-cliente'
    );


const cerrarDatos =
    document.getElementById(
        'cerrar-datos'
    );


// ========================================
// CONTINUAR
// ========================================

btnContinuar.addEventListener(
    'click',
    () => {

        if (carrito.length === 0) {

            alert(
                'Agrega al menos un producto.'
            );

            return;

        }


        resumenPedido.classList.add(
            'oculto'
        );


        datosCliente.classList.remove(
            'oculto'
        );

    }
);


// ========================================
// CERRAR FORMULARIO
// ========================================

cerrarDatos.addEventListener(
    'click',
    () => {

        datosCliente.classList.add(
            'oculto'
        );

    }
);


// ========================================
// DELIVERY / RETIRO
// ========================================

const opcionesEntrega =
    document.querySelectorAll(
        'input[name="tipo-entrega"]'
    );


const direccionContainer =
    document.getElementById(
        'direccion-container'
    );


opcionesEntrega.forEach(opcion => {

    opcion.addEventListener(
        'change',
        () => {

            if (
                opcion.value === 'delivery' &&
                opcion.checked
            ) {

                direccionContainer.classList.remove(
                    'oculto'
                );

            }


            if (
                opcion.value === 'retiro' &&
                opcion.checked
            ) {

                direccionContainer.classList.add(
                    'oculto'
                );

            }

        }
    );

});


// ========================================
// MÉTODOS DE PAGO
// ========================================

const opcionesPago =
    document.querySelectorAll(
        'input[name="metodo-pago"]'
    );


const datosTransferencia =
    document.getElementById(
        'datos-transferencia'
    );


opcionesPago.forEach(opcion => {

    opcion.addEventListener(
        'change',
        () => {

            if (
                opcion.value === 'transferencia' &&
                opcion.checked
            ) {

                datosTransferencia.classList.remove(
                    'oculto'
                );

            } else {

                datosTransferencia.classList.add(
                    'oculto'
                );

            }

        }
    );

});


// ========================================
// CONFIRMAR PEDIDO ONLINE
// ========================================

const confirmarPedido =
    document.getElementById(
        'confirmar-pedido'
    );


confirmarPedido.addEventListener(
    'click',
    () => {


        // -------------------------------
        // DATOS DEL CLIENTE
        // -------------------------------

        const nombre =
            document.getElementById(
                'nombre-cliente'
            ).value.trim();


        const telefono =
            document.getElementById(
                'telefono-cliente'
            ).value.trim();


        // -------------------------------
        // TIPO DE ENTREGA
        // -------------------------------

        const tipoEntregaElemento =
            document.querySelector(
                'input[name="tipo-entrega"]:checked'
            );


        if (!tipoEntregaElemento) {

            alert(
                'Selecciona cómo quieres recibir tu pedido.'
            );

            return;

        }


        const tipoEntrega =
            tipoEntregaElemento.value;


        // -------------------------------
        // DIRECCIÓN
        // -------------------------------

        const direccion =
            document.getElementById(
                'direccion-cliente'
            ).value.trim();


        // -------------------------------
        // MÉTODO DE PAGO
        // -------------------------------

        const metodoPagoElemento =
            document.querySelector(
                'input[name="metodo-pago"]:checked'
            );


        let metodoPago = '';


        if (metodoPagoElemento) {

            metodoPago =
                metodoPagoElemento.value;

        }


        // -------------------------------
        // VALIDACIONES
        // -------------------------------

        if (!nombre) {

            alert(
                'Ingresa tu nombre.'
            );

            return;

        }


        if (!telefono) {

            alert(
                'Ingresa tu teléfono.'
            );

            return;

        }


        if (
            tipoEntrega === 'delivery' &&
            !direccion
        ) {

            alert(
                'Ingresa tu dirección.'
            );

            return;

        }


        if (!metodoPago) {

            alert(
                'Selecciona un método de pago.'
            );

            return;

        }


        // -------------------------------
        // PREPARAR PEDIDO
        // -------------------------------

        const datos =
            new FormData();


        datos.append(
            'nombre_cliente',
            nombre
        );


        datos.append(
            'telefono_cliente',
            telefono
        );


        datos.append(
            'tipo_entrega',
            tipoEntrega
        );


        datos.append(
            'direccion_entrega',
            direccion
        );


        datos.append(
            'metodo_pago',
            metodoPago
        );


        datos.append(
            'productos',
            JSON.stringify(carrito)
        );


        // -------------------------------
        // ENVIAR A DJANGO
        // -------------------------------

        fetch(
            `/pedidos/online/crear/${restauranteId}/`,
            {

                method: 'POST',

                body: datos,

                headers: {

                    'X-CSRFToken':
                        obtenerCSRF()

                }

            }
        )


        .then(response => {

            return response.json();

        })


        .then(data => {

            if (data.success) {

                // ========================================
                // GUARDAR DATOS DEL PEDIDO
                // ========================================

                localStorage.setItem(
                    'pedidoExitoso',
                    JSON.stringify({
                        pedido_id: data.pedido_id,
                        seguimiento_url: data.seguimiento_url
                    })
                );


                // ========================================
                // MOSTRAR MENSAJE
                // ========================================

                mostrarPedidoExitoso(
                    data.pedido_id,
                    data.seguimiento_url
                );


                // ========================================
                // LIMPIAR CARRITO
                // ========================================

                carrito = [];

                actualizarCarrito();


                datosCliente.classList.add(
                    'oculto'
                );

            } else {

                alert(
                    data.error ||
                    'No se pudo crear el pedido.'
                );

            }

        })


        .catch(error => {

            console.error(
                'Error:',
                error
            );


            alert(
                'Ocurrió un error al enviar el pedido.'
            );

        });

    }
);


// ========================================
// MOSTRAR PEDIDO EXITOSO
// ========================================

function mostrarPedidoExitoso(
    pedidoId,
    seguimientoUrl
) {

    const pedidoExitoso =
        document.getElementById(
            'pedido-exitoso'
        );


    const mensajePedidoExitoso =
        document.getElementById(
            'mensaje-pedido-exitoso'
        );


    const btnSeguimiento =
        document.getElementById(
            'btn-seguimiento'
        );


    if (!pedidoExitoso) {
        return;
    }


    mensajePedidoExitoso.textContent =
        `Tu pedido #${pedidoId} fue recibido correctamente.`;


    if (seguimientoUrl) {

        btnSeguimiento.href =
            seguimientoUrl;

    }


    pedidoExitoso.classList.remove(
        'oculto'
    );

}


// ========================================
// RECUPERAR PEDIDO DESPUÉS DE RECARGAR
// ========================================

document.addEventListener(
    'DOMContentLoaded',
    () => {

        const pedidoGuardado =
            localStorage.getItem(
                'pedidoExitoso'
            );


        if (!pedidoGuardado) {
            return;
        }


        try {

            const pedido =
                JSON.parse(
                    pedidoGuardado
                );


            if (
                pedido.pedido_id &&
                pedido.seguimiento_url
            ) {

                mostrarPedidoExitoso(
                    pedido.pedido_id,
                    pedido.seguimiento_url
                );

            }

        } catch (error) {

            console.error(
                'Error recuperando pedido:',
                error
            );

            localStorage.removeItem(
                'pedidoExitoso'
            );

        }

    }
);


// ========================================
// OBTENER CSRF
// ========================================

function obtenerCSRF() {

    const cookies =
        document.cookie.split(';');


    for (
        let cookie of cookies
    ) {

        cookie =
            cookie.trim();


        if (
            cookie.startsWith(
                'csrftoken='
            )
        ) {

            return decodeURIComponent(
                cookie.substring(
                    'csrftoken='.length
                )
            );

        }

    }


    return '';

}


// ========================================
// COMPROBAR ESTADO DEL PEDIDO GUARDADO
// ========================================

function comprobarPedidoGuardado() {

    const pedidoGuardado =
        localStorage.getItem('pedidoExitoso');


    if (!pedidoGuardado) {
        return;
    }


    let pedido;


    try {

        pedido = JSON.parse(
            pedidoGuardado
        );

    } catch (error) {

        console.error(
            'Error leyendo pedido guardado:',
            error
        );

        localStorage.removeItem(
            'pedidoExitoso'
        );

        return;

    }


    if (!pedido.seguimiento_url) {
        return;
    }


    fetch(
        pedido.seguimiento_url,
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
                'No se pudo consultar el pedido.'
            );

        }

        return response.json();

    })

    .then(data => {

        console.log(
            'Estado actual del pedido:',
            data.estado
        );


        // ========================================
        // PEDIDO TERMINADO
        // ========================================

        if (
            data.estado === 'entregado' ||
            data.estado === 'cancelado'
        ) {

            // Borrar pedido guardado
            localStorage.removeItem(
                'pedidoExitoso'
            );


            // Ocultar mensaje
            const pedidoExitoso =
                document.getElementById(
                    'pedido-exitoso'
                );


            if (pedidoExitoso) {

                pedidoExitoso.classList.add(
                    'oculto'
                );

            }


            return;

        }


        // ========================================
        // PEDIDO TODAVÍA ACTIVO
        // ========================================

        mostrarPedidoExitoso(
            pedido.pedido_id,
            pedido.seguimiento_url
        );

    })

    .catch(error => {

        console.error(
            'Error comprobando pedido:',
            error
        );

    });

}


// ========================================
// COMPROBAR AL CARGAR
// ========================================

document.addEventListener(
    'DOMContentLoaded',
    () => {

        comprobarPedidoGuardado();

    }
);


// ========================================
// COMPROBAR CADA 5 SEGUNDOS
// ========================================

setInterval(
    comprobarPedidoGuardado,
    5000
);