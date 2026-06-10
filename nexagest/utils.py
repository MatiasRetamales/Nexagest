from pedidos.models import Pedido

def testear_bd():
    pedido = Pedido.objects.first()

    if not pedido:
        print("No hay pedidos en la base de datos.")
        return

    print("=== Primer pedido ===")
    print("ID:", pedido.id)

    if pedido.mesa:
        print("Mesa:", pedido.mesa.numero)
    else:
        print("Mesa: Sin mesa asignada")

    if pedido.garzon:
        print("Garzón:", pedido.garzon.username)
    else:
        print("Garzón: No asignado")

    print("Estado:", pedido.estado)
    print("Fecha:", pedido.fecha)