from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from administracion.models import Caja
from carta.models import Categoria, Producto
from core.models import Restaurante
from mesas.models import Mesa
from pedidos.models import Pedido, PedidoItem
from usuarios.models import Perfil


class PedidoFlowTests(TestCase):
    def setUp(self):
        self.restaurante = Restaurante.objects.create(
            nombre="Nexagest Food",
            tipo_local="restaurante",
            propina_activa=True,
            porcentaje_propina=10,
        )
        self.garzon = self.crear_usuario("garzon", "garzon")
        self.cocinero = self.crear_usuario("cocinero", "cocinero")
        self.mesa = Mesa.objects.create(
            numero=1,
            estado="libre",
            restaurante=self.restaurante,
        )
        self.categoria = Categoria.objects.create(
            nombre="Comida",
            restaurante=self.restaurante,
        )
        self.producto = Producto.objects.create(
            nombre="Completo",
            precio=Decimal("2500"),
            disponibilidad="disponible",
            restaurante=self.restaurante,
            categoria=self.categoria,
        )

    def crear_usuario(self, username, rol):
        user = User.objects.create_user(username=username, password="testpass123")
        Perfil.objects.create(
            user=user,
            rol=rol,
            nombre_usuario=username,
            restaurante=self.restaurante,
        )
        return user

    def test_garzon_crea_pedido_con_items_desde_mesa(self):
        self.client.force_login(self.garzon)

        response = self.client.post(
            reverse("gestionar_pedido", args=[self.mesa.id]),
            {
                f"cantidad_{self.producto.id}": "2",
                f"obs_{self.producto.id}": "Sin mayo",
            },
        )

        self.assertRedirects(
            response,
            reverse("gestionar_pedido", args=[self.mesa.id]),
            fetch_redirect_response=False,
        )
        pedido = Pedido.objects.get(mesa=self.mesa, restaurante=self.restaurante)
        item = PedidoItem.objects.get(pedido=pedido)
        self.assertEqual(pedido.estado, "pendiente")
        self.assertEqual(item.producto, self.producto)
        self.assertEqual(item.cantidad, 2)
        self.assertEqual(item.observacion, "Sin mayo")
        self.assertEqual(item.subtotal(), Decimal("5000"))

    def test_enviar_cocina_marca_pedido_e_items(self):
        self.client.force_login(self.garzon)
        pedido = Pedido.objects.create(
            mesa=self.mesa,
            garzon=self.garzon,
            restaurante=self.restaurante,
        )
        item = PedidoItem.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=1,
            precio_unitario=self.producto.precio,
        )

        response = self.client.post(reverse("enviar_cocina", args=[pedido.id]))

        self.assertRedirects(
            response,
            reverse("detalle_mesa", args=[self.mesa.id]),
            fetch_redirect_response=False,
        )
        pedido.refresh_from_db()
        item.refresh_from_db()
        self.assertEqual(pedido.estado, "en_preparacion")
        self.assertEqual(pedido.total_envios, 1)
        self.assertIsNotNone(pedido.enviado_a_cocina)
        self.assertTrue(item.enviado_a_cocina)
        self.assertEqual(item.numero_envio, 1)

    def test_cerrar_pedido_con_propina_asocia_caja_y_marca_pagado(self):
        self.client.force_login(self.garzon)
        caja = Caja.objects.create(
            restaurante=self.restaurante,
            monto_inicial=Decimal("10000"),
            saldo_actual=Decimal("10000"),
            esta_abierta=True,
            nombre_cajero="admin",
        )
        pedido = Pedido.objects.create(
            mesa=self.mesa,
            garzon=self.garzon,
            restaurante=self.restaurante,
            estado="listo",
        )
        PedidoItem.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=2,
            precio_unitario=self.producto.precio,
        )

        response = self.client.post(
            reverse("cerrar_pedido", args=[self.mesa.id]),
            {"usar_propina": "1"},
        )

        self.assertRedirects(response, reverse("lista_mesas"), fetch_redirect_response=False)
        pedido.refresh_from_db()
        self.assertTrue(pedido.esta_pagado)
        self.assertTrue(pedido.propina_aplicada)
        self.assertEqual(pedido.monto_propina, Decimal("500.0"))
        self.assertEqual(pedido.total, Decimal("5500.0"))
        self.assertEqual(pedido.sesion_caja, caja)
        self.assertIsNotNone(pedido.fecha_pago)

    def test_operador_puede_ver_cocina_marcar_listo_y_cobrar(self):
        operador = self.crear_usuario("operador", "operador")
        self.client.force_login(operador)
        Caja.objects.create(
            restaurante=self.restaurante,
            monto_inicial=Decimal("10000"),
            saldo_actual=Decimal("10000"),
            esta_abierta=True,
            nombre_cajero="admin",
        )
        pedido = Pedido.objects.create(
            mesa=self.mesa,
            garzon=operador,
            restaurante=self.restaurante,
            estado="en_preparacion",
            total_envios=1,
        )
        PedidoItem.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=1,
            precio_unitario=self.producto.precio,
            enviado_a_cocina=True,
            numero_envio=1,
        )

        response = self.client.get(reverse("cocina"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse("marcar_pedido_listo", args=[pedido.id]))
        self.assertRedirects(response, reverse("cocina"), fetch_redirect_response=False)
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, "listo")

        response = self.client.post(
            reverse("cerrar_pedido", args=[self.mesa.id]),
            {"usar_propina": "0"},
        )
        self.assertRedirects(response, reverse("lista_mesas"), fetch_redirect_response=False)
        pedido.refresh_from_db()
        self.assertTrue(pedido.esta_pagado)
        self.assertEqual(pedido.total, Decimal("2500"))

    def test_marcar_pedido_listo_redirige_a_cocina(self):
        self.client.force_login(self.cocinero)
        pedido = Pedido.objects.create(
            mesa=self.mesa,
            garzon=self.garzon,
            restaurante=self.restaurante,
            estado="en_preparacion",
        )

        response = self.client.post(reverse("marcar_pedido_listo", args=[pedido.id]))

        self.assertRedirects(response, reverse("cocina"), fetch_redirect_response=False)
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, "listo")
