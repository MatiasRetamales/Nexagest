function marcarPedidoListo(pedidoId) {
    // 1. Buscamos la tarjeta por el número
    const tarjeta = document.getElementById(pedidoId);

     
    
    // 2. Hacemos el fetch a la URL que espera el número
    fetch(`/pedidos/listo/${pedidoId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.ok) {
            // 3. Si todo salió bien en Django, borramos visualmente
            tarjeta.style.transition = "all 0.4s ease";
            tarjeta.style.opacity = "0";
            setTimeout(() => tarjeta.remove(), 400);
        } else {
            alert("Pedido Listo");
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