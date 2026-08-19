let carrito = [];


// ========================================
// AGREGAR PRODUCTOS
// ========================================

const botonesAgregar =
    document.querySelectorAll(".btn-agregar");


botonesAgregar.forEach((boton) => {

    boton.addEventListener("click", () => {

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


    carrito.forEach((producto) => {

        cantidadTotal +=
            producto.cantidad;

        precioTotal +=
            producto.precio *
            producto.cantidad;

    });


    const cantidadCarrito =
        document.getElementById(
            "cantidad-carrito"
        );


    const totalCarrito =
        document.getElementById(
            "total-carrito"
        );


    if (cantidadCarrito) {

        cantidadCarrito.textContent =
            `${cantidadTotal} productos`;

    }


    if (totalCarrito) {

        totalCarrito.textContent =
            `$${precioTotal.toLocaleString("es-CL")}`;

    }

}



// ========================================
// ELEMENTOS DEL PEDIDO
// ========================================

const btnCarrito =
    document.getElementById(
        "btn-carrito"
    );


const resumenPedido =
    document.getElementById(
        "resumen-pedido"
    );


const cerrarPedido =
    document.getElementById(
        "cerrar-pedido"
    );


const listaPedido =
    document.getElementById(
        "lista-pedido"
    );


const totalPedido =
    document.getElementById(
        "total-pedido"
    );



// ========================================
// ABRIR RESUMEN
// ========================================

if (btnCarrito) {

    btnCarrito.addEventListener(
        "click",
        () => {

            if (carrito.length === 0) {

                alert(
                    "Agrega al menos un producto."
                );

                return;

            }


            actualizarResumenPedido();


            resumenPedido.classList.remove(
                "oculto"
            );

        }
    );

}



// ========================================
// ACTUALIZAR RESUMEN DEL PEDIDO
// ========================================

function actualizarResumenPedido() {

    if (!listaPedido || !totalPedido) {

        return;

    }


    listaPedido.innerHTML = "";

    let total = 0;



    carrito.forEach((producto) => {

        const subtotal =
            producto.precio *
            producto.cantidad;


        total += subtotal;



        listaPedido.innerHTML += `

            <div
                class="item-pedido"
                data-id="${producto.id}"
            >

                <div class="item-pedido-info">

                    <strong>
                        ${producto.nombre}
                    </strong>


                    <span>
                        $${producto.precio.toLocaleString("es-CL")}
                        c/u
                    </span>

                </div>


                <div class="item-pedido-controles">

                    <button
                        type="button"
                        class="btn-cantidad btn-restar"
                        data-id="${producto.id}"
                        aria-label="Disminuir cantidad"
                    >

                        −

                    </button>


                    <span class="cantidad-producto">

                        ${producto.cantidad}

                    </span>


                    <button
                        type="button"
                        class="btn-cantidad btn-sumar"
                        data-id="${producto.id}"
                        aria-label="Aumentar cantidad"
                    >

                        +

                    </button>


                    <strong class="subtotal-producto">

                        $${subtotal.toLocaleString("es-CL")}

                    </strong>


                    <button
                        type="button"
                        class="btn-eliminar-producto"
                        data-id="${producto.id}"
                        aria-label="Eliminar ${producto.nombre}"
                    >

                        ×

                    </button>

                </div>

            </div>

        `;

    });



    totalPedido.textContent =
        `$${total.toLocaleString("es-CL")}`;



    // ========================================
    // BOTONES RESTAR
    // ========================================

    const botonesRestar =
        listaPedido.querySelectorAll(
            ".btn-restar"
        );


    botonesRestar.forEach((boton) => {

        boton.addEventListener(
            "click",
            () => {

                const id =
                    boton.dataset.id;


                const producto =
                    carrito.find(
                        producto =>
                            producto.id === id
                    );


                if (!producto) {

                    return;

                }


                producto.cantidad -= 1;



                if (producto.cantidad <= 0) {

                    carrito =
                        carrito.filter(
                            producto =>
                                producto.id !== id
                        );

                }


                actualizarCarrito();

                actualizarResumenPedido();

            }
        );

    });



    // ========================================
    // BOTONES SUMAR
    // ========================================

    const botonesSumar =
        listaPedido.querySelectorAll(
            ".btn-sumar"
        );


    botonesSumar.forEach((boton) => {

        boton.addEventListener(
            "click",
            () => {

                const id =
                    boton.dataset.id;


                const producto =
                    carrito.find(
                        producto =>
                            producto.id === id
                    );


                if (!producto) {

                    return;

                }


                producto.cantidad += 1;


                actualizarCarrito();

                actualizarResumenPedido();

            }
        );

    });



    // ========================================
    // BOTONES ELIMINAR
    // ========================================

    const botonesEliminar =
        listaPedido.querySelectorAll(
            ".btn-eliminar-producto"
        );


    botonesEliminar.forEach((boton) => {

        boton.addEventListener(
            "click",
            () => {

                const id =
                    boton.dataset.id;


                carrito =
                    carrito.filter(
                        producto =>
                            producto.id !== id
                    );


                actualizarCarrito();

                actualizarResumenPedido();

            }
        );

    });

}



// ========================================
// CERRAR RESUMEN
// ========================================

if (cerrarPedido) {

    cerrarPedido.addEventListener(
        "click",
        () => {

            resumenPedido.classList.add(
                "oculto"
            );

        }
    );

}



// ========================================
// FORMULARIO CLIENTE
// ========================================

const btnContinuar =
    document.getElementById(
        "btn-continuar"
    );


const datosCliente =
    document.getElementById(
        "datos-cliente"
    );


const cerrarDatos =
    document.getElementById(
        "cerrar-datos"
    );



// ========================================
// CONTINUAR
// ========================================

if (btnContinuar) {

    btnContinuar.addEventListener(
        "click",
        () => {

            if (carrito.length === 0) {

                alert(
                    "Agrega al menos un producto."
                );

                return;

            }


            resumenPedido.classList.add(
                "oculto"
            );


            datosCliente.classList.remove(
                "oculto"
            );


            actualizarMetodosPago();

        }
    );

}



// ========================================
// CERRAR FORMULARIO
// ========================================

if (cerrarDatos) {

    cerrarDatos.addEventListener(
        "click",
        () => {

            datosCliente.classList.add(
                "oculto"
            );

        }
    );

}



// ========================================
// DELIVERY / RETIRO
// ========================================

const opcionesEntrega =
    document.querySelectorAll(
        'input[name="tipo-entrega"]'
    );


const direccionContainer =
    document.getElementById(
        "direccion-container"
    );


opcionesEntrega.forEach((opcion) => {

    opcion.addEventListener(
        "change",
        () => {

            if (
                opcion.value === "delivery" &&
                opcion.checked
            ) {

                direccionContainer.classList.remove(
                    "oculto"
                );

            }


            if (
                opcion.value === "retiro" &&
                opcion.checked
            ) {

                direccionContainer.classList.add(
                    "oculto"
                );

            }


            actualizarMetodosPago();

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
        "datos-transferencia"
    );


const avisoMetodosPago =
    document.getElementById(
        "aviso-metodos-pago"
    );



// ========================================
// ACTUALIZAR MÉTODOS DE PAGO
// ========================================

function actualizarMetodosPago() {

    const tipoEntregaElemento =
        document.querySelector(
            'input[name="tipo-entrega"]:checked'
        );


    if (!tipoEntregaElemento) {

        return;

    }


    const tipoEntrega =
        tipoEntregaElemento.value;


    let hayMetodoDisponible = false;


    let primerMetodoDisponible = null;



    // ========================================
    // REVISAR CADA MÉTODO
    // ========================================

    opcionesPago.forEach((opcion) => {

        const label =
            opcion.parentElement;


        if (!label) {

            return;

        }


        let disponible = false;



        // ----------------------------------------
        // RETIRO
        // ----------------------------------------

        if (tipoEntrega === "retiro") {

            disponible =
                label.dataset.retiro === "true";

        }



        // ----------------------------------------
        // DELIVERY
        // ----------------------------------------

        if (tipoEntrega === "delivery") {

            disponible =
                label.dataset.delivery === "true";

        }



        // ----------------------------------------
        // MOSTRAR / OCULTAR
        // ----------------------------------------

        if (disponible) {

            label.classList.remove(
                "oculto"
            );


            hayMetodoDisponible = true;


            if (!primerMetodoDisponible) {

                primerMetodoDisponible =
                    opcion;

            }

        } else {

            label.classList.add(
                "oculto"
            );


            opcion.checked = false;

        }

    });



    // ========================================
    // SI NO HAY MÉTODOS
    // ========================================

    if (hayMetodoDisponible) {

        if (avisoMetodosPago) {

            avisoMetodosPago.classList.add(
                "oculto"
            );

        }

    } else {

        if (avisoMetodosPago) {

            avisoMetodosPago.classList.remove(
                "oculto"
            );

        }

    }



    // ========================================
    // SELECCIONAR MÉTODO AUTOMÁTICAMENTE
    // ========================================

    const metodoSeleccionado =
        document.querySelector(
            'input[name="metodo-pago"]:checked'
        );


    if (
        !metodoSeleccionado ||
        metodoSeleccionado.parentElement.classList.contains(
            "oculto"
        )
    ) {

        if (primerMetodoDisponible) {

            primerMetodoDisponible.checked = true;

        }

    }



    // ========================================
    // DATOS TRANSFERENCIA
    // ========================================

    const transferenciaSeleccionada =
        document.querySelector(
            'input[name="metodo-pago"][value="transferencia"]:checked'
        );


    if (
        transferenciaSeleccionada &&
        datosTransferencia
    ) {

        datosTransferencia.classList.remove(
            "oculto"
        );

    } else if (datosTransferencia) {

        datosTransferencia.classList.add(
            "oculto"
        );

    }

}



// ========================================
// CAMBIO DE MÉTODO DE PAGO
// ========================================

opcionesPago.forEach((opcion) => {

    opcion.addEventListener(
        "change",
        () => {

            if (
                opcion.value === "transferencia" &&
                opcion.checked
            ) {

                if (datosTransferencia) {

                    datosTransferencia.classList.remove(
                        "oculto"
                    );

                }

            } else {

                if (datosTransferencia) {

                    datosTransferencia.classList.add(
                        "oculto"
                    );

                }

            }

        }
    );

});



// ========================================
// CONFIRMAR PEDIDO ONLINE
// ========================================

const confirmarPedido =
    document.getElementById(
        "confirmar-pedido"
    );


if (confirmarPedido) {

    confirmarPedido.addEventListener(
        "click",
        async () => {


            // ========================================
            // DATOS CLIENTE
            // ========================================

            const nombre =
                document.getElementById(
                    "nombre-cliente"
                ).value.trim();


            const telefono =
                document.getElementById(
                    "telefono-cliente"
                ).value.trim();



            // ========================================
            // TIPO ENTREGA
            // ========================================

            const tipoEntregaElemento =
                document.querySelector(
                    'input[name="tipo-entrega"]:checked'
                );


            if (!tipoEntregaElemento) {

                alert(
                    "Selecciona cómo quieres recibir tu pedido."
                );

                return;

            }


            const tipoEntrega =
                tipoEntregaElemento.value;



            // ========================================
            // DIRECCIÓN
            // ========================================

            const direccion =
                document.getElementById(
                    "direccion-cliente"
                ).value.trim();



            // ========================================
            // MÉTODO PAGO
            // ========================================

            const metodoPagoElemento =
                document.querySelector(
                    'input[name="metodo-pago"]:checked'
                );


            let metodoPago = "";


            if (metodoPagoElemento) {

                metodoPago =
                    metodoPagoElemento.value;

            }



            // ========================================
            // VALIDACIONES
            // ========================================

            if (!nombre) {

                alert(
                    "Ingresa tu nombre."
                );

                return;

            }


            if (!telefono) {

                alert(
                    "Ingresa tu teléfono."
                );

                return;

            }


            if (
                tipoEntrega === "delivery" &&
                !direccion
            ) {

                alert(
                    "Ingresa tu dirección."
                );

                return;

            }


            if (!metodoPago) {

                alert(
                    "Selecciona un método de pago."
                );

                return;

            }


            if (carrito.length === 0) {

                alert(
                    "El carrito está vacío."
                );

                return;

            }



            // ========================================
            // PREPARAR PEDIDO
            // ========================================

            const datos =
                new FormData();


            datos.append(
                "nombre_cliente",
                nombre
            );


            datos.append(
                "telefono_cliente",
                telefono
            );


            datos.append(
                "tipo_entrega",
                tipoEntrega
            );


            datos.append(
                "direccion_entrega",
                direccion
            );


            datos.append(
                "metodo_pago",
                metodoPago
            );


            datos.append(
                "productos",
                JSON.stringify(carrito)
            );



            // ========================================
            // CSRF
            // ========================================

            const tokenCSRF =
                csrfToken;


            console.log(
                "Restaurante:",
                restauranteId
            );


            console.log(
                "CSRF:",
                tokenCSRF
            );


            console.log(
                "Carrito:",
                carrito
            );


            if (!tokenCSRF) {

                alert(
                    "No se pudo obtener el token de seguridad. Recarga la página."
                );

                return;

            }



            // ========================================
            // DESACTIVAR BOTÓN
            // ========================================

            confirmarPedido.disabled =
                true;


            confirmarPedido.textContent =
                "Enviando pedido...";



            try {


                // ========================================
                // ENVIAR A DJANGO
                // ========================================

                const response =
                    await fetch(
                        `/pedidos/online/crear/${restauranteId}/`,
                        {
                            method: "POST",

                            body: datos,

                            credentials:
                                "same-origin",

                            headers: {

                                "X-CSRFToken":
                                    tokenCSRF,

                                "X-Requested-With":
                                    "XMLHttpRequest"

                            }

                        }
                    );



                // ========================================
                // LEER RESPUESTA
                // ========================================

                const contentType =
                    response.headers.get(
                        "content-type"
                    ) || "";


                if (
                    !contentType.includes(
                        "application/json"
                    )
                ) {

                    const texto =
                        await response.text();


                    console.error(
                        "Respuesta no JSON:",
                        texto
                    );


                    if (
                        response.status === 403
                    ) {

                        throw new Error(
                            "Django rechazó la petición por CSRF (403)."
                        );

                    }


                    throw new Error(
                        `El servidor respondió con HTTP ${response.status}.`
                    );

                }


                const data =
                    await response.json();



                // ========================================
                // PEDIDO CREADO
                // ========================================

                if (data.success) {

                    localStorage.setItem(
                        "pedidoExitoso",

                        JSON.stringify({

                            pedido_id:
                                data.pedido_id,

                            seguimiento_url:
                                data.seguimiento_url

                        })
                    );


                    mostrarPedidoExitoso(
                        data.pedido_id,
                        data.seguimiento_url
                    );


                    carrito = [];


                    actualizarCarrito();


                    datosCliente.classList.add(
                        "oculto"
                    );


                } else {

                    alert(
                        data.error ||
                        "No se pudo crear el pedido."
                    );

                }


            } catch (error) {

                console.error(
                    "Error enviando pedido:",
                    error
                );


                alert(
                    error.message ||
                    "Ocurrió un error al enviar el pedido."
                );


            } finally {

                confirmarPedido.disabled =
                    false;


                confirmarPedido.textContent =
                    "Confirmar pedido";

            }

        }
    );

}



// ========================================
// MOSTRAR PEDIDO EXITOSO
// ========================================

function mostrarPedidoExitoso(
    pedidoId,
    seguimientoUrl
) {

    const pedidoExitoso =
        document.getElementById(
            "pedido-exitoso"
        );


    const mensajePedidoExitoso =
        document.getElementById(
            "mensaje-pedido-exitoso"
        );


    const btnSeguimiento =
        document.getElementById(
            "btn-seguimiento"
        );


    if (!pedidoExitoso) {

        return;

    }


    if (mensajePedidoExitoso) {

        mensajePedidoExitoso.textContent =
            `Tu pedido #${pedidoId} fue recibido correctamente.`;

    }


    if (
        seguimientoUrl &&
        btnSeguimiento
    ) {

        btnSeguimiento.href =
            seguimientoUrl;

    }


    pedidoExitoso.classList.remove(
        "oculto"
    );

}



// ========================================
// RECUPERAR PEDIDO DESPUÉS DE RECARGAR
// ========================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const pedidoGuardado =
            localStorage.getItem(
                "pedidoExitoso"
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
                "Error recuperando pedido:",
                error
            );


            localStorage.removeItem(
                "pedidoExitoso"
            );

        }

    }
);



// ========================================
// COMPROBAR ESTADO DEL PEDIDO
// ========================================

function comprobarPedidoGuardado() {

    const pedidoGuardado =
        localStorage.getItem(
            "pedidoExitoso"
        );


    if (!pedidoGuardado) {

        return;

    }


    let pedido;


    try {

        pedido =
            JSON.parse(
                pedidoGuardado
            );

    } catch (error) {

        console.error(
            "Error leyendo pedido:",
            error
        );


        localStorage.removeItem(
            "pedidoExitoso"
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

                "X-Requested-With":
                    "XMLHttpRequest"

            }

        }
    )


    .then((response) => {

        if (!response.ok) {

            throw new Error(
                "No se pudo consultar el pedido."
            );

        }


        return response.json();

    })


    .then((data) => {

        console.log(
            "Estado actual:",
            data.estado
        );



        // ========================================
        // PEDIDO TERMINADO
        // ========================================

        if (
            data.estado === "entregado" ||
            data.estado === "cancelado"
        ) {

            localStorage.removeItem(
                "pedidoExitoso"
            );


            const pedidoExitoso =
                document.getElementById(
                    "pedido-exitoso"
                );


            if (pedidoExitoso) {

                pedidoExitoso.classList.add(
                    "oculto"
                );

            }


            return;

        }



        // ========================================
        // PEDIDO ACTIVO
        // ========================================

        mostrarPedidoExitoso(
            pedido.pedido_id,
            pedido.seguimiento_url
        );

    })


    .catch((error) => {

        console.error(
            "Error comprobando pedido:",
            error
        );

    });

}



// ========================================
// COMPROBAR AL CARGAR
// ========================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        comprobarPedidoGuardado();

        actualizarMetodosPago();

    }
);



// ========================================
// COMPROBAR CADA 5 SEGUNDOS
// ========================================

setInterval(
    comprobarPedidoGuardado,
    5000
);



// ========================================
// NAVEGACIÓN POR CATEGORÍAS
// ========================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const botonesCategorias =
            document.querySelectorAll(
                ".categoria-btn"
            );


        const categorias =
            document.querySelectorAll(
                ".categoria"
            );


        if (
            botonesCategorias.length === 0 ||
            categorias.length === 0
        ) {

            return;

        }



        // ========================================
        // CLICK EN CATEGORÍA
        // ========================================

        botonesCategorias.forEach(
            (boton) => {

                boton.addEventListener(
                    "click",
                    () => {

                        const targetId =
                            boton.dataset.target;


                        const categoria =
                            document.getElementById(
                                targetId
                            );


                        if (!categoria) {

                            console.error(
                                "No se encontró la categoría:",
                                targetId
                            );

                            return;

                        }



                        botonesCategorias.forEach(
                            (btn) => {

                                btn.classList.remove(
                                    "activo"
                                );

                            }
                        );


                        boton.classList.add(
                            "activo"
                        );



                        const offset = 75;


                        const posicion =
                            categoria.getBoundingClientRect().top +
                            window.scrollY -
                            offset;


                        window.scrollTo({

                            top: posicion,

                            behavior: "smooth"

                        });

                    }
                );

            }
        );



        // ========================================
        // CAMBIAR CATEGORÍA SEGÚN SCROLL
        // ========================================

        const observer =
            new IntersectionObserver(
                (entries) => {

                    entries.forEach(
                        (entry) => {

                            if (
                                !entry.isIntersecting
                            ) {

                                return;

                            }


                            const categoriaId =
                                entry.target.id;


                            botonesCategorias.forEach(
                                (boton) => {

                                    boton.classList.remove(
                                        "activo"
                                    );


                                    if (
                                        boton.dataset.target ===
                                        categoriaId
                                    ) {

                                        boton.classList.add(
                                            "activo"
                                        );


                                        boton.scrollIntoView({

                                            behavior: "smooth",

                                            block: "nearest",

                                            inline: "center"

                                        });

                                    }

                                }
                            );

                        }
                    );

                },
                {
                    root: null,

                    threshold: 0.15,

                    rootMargin:
                        "-80px 0px -60% 0px"
                }
            );



        // ========================================
        // OBSERVAR CATEGORÍAS
        // ========================================

        categorias.forEach(
            (categoria) => {

                observer.observe(
                    categoria
                );

            }
        );

    }
);