function marcarPedidoListo(pedidoId) {
    const tarjeta = document.getElementById(pedidoId);

    fetch(`/pedidos/listo/${pedidoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert("Error al marcar el pedido como listo");
        }
    })
    .catch(error => console.error('Error:', error));
}






// Esta función busca el token de seguridad que Django guarda en las cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // ¿Esta cookie es la que estamos buscando (csrftoken)?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}