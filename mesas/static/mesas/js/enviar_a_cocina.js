function enviarPedidoACocina(pedidoId) {
    // 1. Una validación de seguridad por si acaso
    if (!pedidoId) {
        alert("No hay un pedido activo para enviar.");
        return;
    }

    // 2. Preguntar al garzón para evitar envíos accidentales
    if (!confirm("¿Estás seguro de enviar este pedido a cocina?")) {
        return;
    }

    // 3. Aquí empieza el "viaje" al servidor
    // Apuntamos a la URL de la otra app (Pedidos)
    fetch(`/pedidos/enviar-a-cocina/${pedidoId}/`, {
        method: 'POST',
        headers: {
            // Django necesita esto por seguridad (CSRF)
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })


    .then(response => {
        if (response.ok) {
            alert("✅ Pedido enviado correctamente");
            location.reload(); // Refrescamos para ver los cambios
        } else {
            alert("❌ Hubo un error al enviar el pedido");
        }
    })
    .catch(error => {
        console.error("Error en la petición:", error);
        alert("Error de conexión con el servidor");
    });
}







function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



