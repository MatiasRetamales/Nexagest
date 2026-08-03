from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from administracion.models import Caja
from core.models import Restaurante
from mesas.models import Mesa
from pedidos.models import Pedido
from usuarios.models import Perfil


class CajaTests(TestCase):
    def setUp(self):
        self.restaurante = Restaurante.objects.create(nombre="Nexagest Food")
        self.admin = User.objects.create_user(username="admin", password="testpass123")
        Perfil.objects.create(
            user=self.admin,
            rol="administrador",
            nombre_usuario="admin",
            restaurante=self.restaurante,
        )
        self.mesa = Mesa.objects.create(numero=1, restaurante=self.restaurante)
        self.client.force_login(self.admin)

    def test_abrir_caja_crea_sesion_abierta(self):
        response = self.client.post(reverse("abrir_caja"), {"monto_inicial": "15000"})

        self.assertRedirects(response, reverse("caja"), fetch_redirect_response=False)
        caja = Caja.objects.get(restaurante=self.restaurante)
        self.assertTrue(caja.esta_abierta)
        self.assertEqual(caja.monto_inicial, Decimal("15000"))
        self.assertEqual(caja.saldo_actual, Decimal("15000"))
        self.assertEqual(caja.nombre_cajero, self.admin.username)

    def test_cerrar_caja_suma_ventas_pagadas_de_la_sesion(self):
        caja = Caja.objects.create(
            restaurante=self.restaurante,
            monto_inicial=Decimal("10000"),
            saldo_actual=Decimal("10000"),
            esta_abierta=True,
            nombre_cajero=self.admin.username,
        )
        Pedido.objects.create(
            mesa=self.mesa,
            garzon=self.admin,
            restaurante=self.restaurante,
            esta_pagado=True,
            total=Decimal("7500"),
            sesion_caja=caja,
        )

        response = self.client.post(reverse("cerrar_caja"))

        self.assertRedirects(response, reverse("caja"), fetch_redirect_response=False)
        caja.refresh_from_db()
        self.assertFalse(caja.esta_abierta)
        self.assertEqual(caja.saldo_actual, Decimal("17500"))
        self.assertIsNotNone(caja.fecha_cierre)

    def test_admin_crea_operador(self):
        response = self.client.post(
            reverse("agregar_operador"),
            {"nombre": "operador", "contraseña": "testpass123"},
        )

        self.assertRedirects(
            response,
            reverse("gestionar_operadores"),
            fetch_redirect_response=False,
        )
        perfil = Perfil.objects.get(user__username="operador")
        self.assertEqual(perfil.rol, "operador")
        self.assertEqual(perfil.restaurante, self.restaurante)
        self.assertTrue(perfil.activo)

    def test_operador_no_puede_abrir_caja(self):
        operador = User.objects.create_user(username="operador", password="testpass123")
        Perfil.objects.create(
            user=operador,
            rol="operador",
            nombre_usuario="operador",
            restaurante=self.restaurante,
        )
        self.client.force_login(operador)

        response = self.client.post(reverse("abrir_caja"), {"monto_inicial": "15000"})

        self.assertRedirects(response, "/login/", fetch_redirect_response=False)
        self.assertFalse(Caja.objects.filter(restaurante=self.restaurante).exists())
