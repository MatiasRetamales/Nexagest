document.addEventListener("DOMContentLoaded", () => {
    const buscador = document.getElementById("buscador");
    const contenedor = document.querySelector(".contenedor-productos");

    buscador.addEventListener("input", () => {
        const texto = buscador.value.toLowerCase().trim();
        const productos = document.querySelectorAll(".product-card");
        const botonesCat = document.querySelectorAll(".btn-cat");

        if (texto === "") {
            // Si el buscador se vacía, mostramos TODOS o podrías llamar a filtrarProductos('todos')
            productos.forEach(p => {
                p.classList.remove("hidden");
                p.style.display = "flex";
            });
            botonesCat.forEach(b => b.classList.remove("active"));
            // Opcional: marcar el botón 'todos' como activo
            document.querySelector('.btn-todos')?.classList.add("active");
            return;
        }

        // --- EL CAMBIO CLAVE ---
        // Al empezar a escribir, quitamos la selección de cualquier categoría 
        // para buscar en todo el inventario.
        botonesCat.forEach(b => b.classList.remove("active"));

        productos.forEach(producto => {
            const nombre = producto.getAttribute("data-nombre");
            
            // Si el nombre coincide con la búsqueda
            if (nombre.includes(texto)) {
                producto.classList.remove("hidden");
                producto.style.display = "flex"; 
            } else {
                producto.classList.add("hidden");
                producto.style.display = "none";
            }
        });
    });

    // --- NUEVAS FUNCIONES PARA EL TECLADO ---

    // B. Cerrar teclado al empezar a deslizar hacia abajo (Scroll)
    // Muy útil cuando salen los resultados y el garzón baja para elegir uno
    window.addEventListener("scroll", () => {
        if (document.activeElement === buscador) {
            buscador.blur();
        }
    }, { passive: true });
});

/**
 * Lógica de Categorías
 */
function filtrarProductos(categoriaId, botonActivo) {
    const productos = document.querySelectorAll(".product-card");
    const botones = document.querySelectorAll(".btn-cat");
    const buscador = document.getElementById("buscador");

    // Si elijo una categoría, borro lo que haya en el buscador
    buscador.value = "";

    botones.forEach(b => b.classList.remove("active"));
    if (botonActivo) botonActivo.classList.add("active");

    productos.forEach(producto => {
        const coincideCategoria = (categoriaId === 'todos' || producto.classList.contains('categoria-' + categoriaId));

        if (coincideCategoria) {
            producto.classList.remove("hidden");
            producto.style.display = "flex"; 
        } else {
            producto.classList.add("hidden");
            producto.style.display = "none";
        }
    });
}








