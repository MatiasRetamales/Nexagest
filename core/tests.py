from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Restaurante
from usuarios.models import Perfil


class DespachoUsuarioTests(TestCase):
    def setUp(self):
        self.restaurante = Restaurante.objects.create(nombre="Nexagest Food")

    def crear_usuario(self, username, rol):
        user = User.objects.create_user(username=username, password="testpass123")
        Perfil.objects.create(
            user=user,
            rol=rol,
            nombre_usuario=username,
            restaurante=self.restaurante,
        )
        return user

    def test_redirige_garzon_a_lista_mesas(self):
        self.client.force_login(self.crear_usuario("garzon", "garzon"))

        response = self.client.get(reverse("despacho"))

        self.assertRedirects(response, reverse("lista_mesas"), fetch_redirect_response=False)

    def test_redirige_operador_a_lista_mesas(self):
        self.client.force_login(self.crear_usuario("operador", "operador"))

        response = self.client.get(reverse("despacho"))

        self.assertRedirects(response, reverse("lista_mesas"), fetch_redirect_response=False)

    def test_redirige_cocinero_a_cocina(self):
        self.client.force_login(self.crear_usuario("cocinero", "cocinero"))

        response = self.client.get(reverse("despacho"))

        self.assertRedirects(response, reverse("cocina"), fetch_redirect_response=False)

    def test_redirige_administrador_a_menu_admin(self):
        self.client.force_login(self.crear_usuario("admin", "administrador"))

        response = self.client.get(reverse("despacho"))

        self.assertRedirects(response, reverse("menu_admin"), fetch_redirect_response=False)
