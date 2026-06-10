/**
 * Incrementa la cantidad de un producto
 */
function sumarUno(productoId) {
    const inputCantidad = document.getElementById('cant_' + productoId);
    const badge = document.getElementById('badge_' + productoId);
    
    // Convertimos a entero y sumamos
    let nuevaCantidad = parseInt(inputCantidad.value) + 1;
    
    // Actualizamos los elementos
    inputCantidad.value = nuevaCantidad;
    badge.innerText = nuevaCantidad;
    
    // Aplicamos los cambios visuales
    actualizarEstiloTarjeta(productoId, nuevaCantidad);
}

/**
 * Decrementa la cantidad de un producto (mínimo 0)
 */
function restarUno(productoId) {
    const inputCantidad = document.getElementById('cant_' + productoId);
    const badge = document.getElementById('badge_' + productoId);
    
    let cantidadActual = parseInt(inputCantidad.value);
    
    // Solo restamos si es mayor a cero para evitar números negativos
    if (cantidadActual > 0) {
        let nuevaCantidad = cantidadActual - 1;
        
        inputCantidad.value = nuevaCantidad;
        badge.innerText = nuevaCantidad;
        
        // Aplicamos los cambios visuales
        actualizarEstiloTarjeta(productoId, nuevaCantidad);
    }
}

/**
 * Función auxiliar para manejar el diseño de la tarjeta según la cantidad
 */
function actualizarEstiloTarjeta(productoId, cantidad) {
    const badge = document.getElementById('badge_' + productoId);
    const inputCantidad = document.getElementById('cant_' + productoId);
    const tarjeta = inputCantidad.closest('.product-card');
    
    if (cantidad > 0) {
        // Estado Activo (Verde Cartagena)
        badge.style.backgroundColor = "#31c253"; 
        badge.style.color = "white";
        badge.style.fontWeight = "bold";
        tarjeta.style.boxShadow = "0 8px 16px rgba(49, 194, 83, 0.3)";
        tarjeta.style.transform = "translateY(-4px)"; // Pequeña elevación
    } else {
        // Estado Inactivo (Gris neutro)
        badge.style.backgroundColor = "#f0f2f5";
        badge.style.color = "#333";
        badge.style.fontWeight = "normal";
        tarjeta.style.boxShadow = "none";
        tarjeta.style.transform = "translateY(0)";
    }
}