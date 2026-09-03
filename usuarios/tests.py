from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import RegistroUsuarioForm


class RegistroUsuarioFormTests(TestCase):
    def test_form_valido_com_dados_corretos(self):
        form = RegistroUsuarioForm(
            data={
                "username": "joao",
                "email": "joao@example.com",
                "password1": "senhaSegura123",
                "password2": "senhaSegura123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalido_com_senhas_diferentes(self):
        form = RegistroUsuarioForm(
            data={
                "username": "joao",
                "email": "joao@example.com",
                "password1": "senhaSegura123",
                "password2": "outraSenha456",
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_invalido_sem_email(self):
        form = RegistroUsuarioForm(
            data={
                "username": "joao",
                "email": "",
                "password1": "senhaSegura123",
                "password2": "senhaSegura123",
            }
        )
        self.assertFalse(form.is_valid())


class RegistrarViewTests(TestCase):
    def test_get_exibe_formulario(self):
        response = self.client.get(reverse("registrar"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], RegistroUsuarioForm)

    def test_post_com_dados_validos_cria_usuario_e_redireciona(self):
        response = self.client.post(
            reverse("registrar"),
            {
                "username": "joao",
                "email": "joao@example.com",
                "password1": "senhaSegura123",
                "password2": "senhaSegura123",
            },
        )
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="joao").exists())

    def test_post_com_dados_invalidos_nao_cria_usuario(self):
        response = self.client.post(
            reverse("registrar"),
            {
                "username": "joao",
                "email": "joao@example.com",
                "password1": "senhaSegura123",
                "password2": "diferente",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="joao").exists())


class LogarViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="senhaSegura123")

    def test_get_exibe_formulario_de_login(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_com_credenciais_validas_redireciona_para_dashboard(self):
        response = self.client.post(
            reverse("login"), {"username": "joao", "password": "senhaSegura123"}
        )
        self.assertRedirects(response, reverse("dashboard"))

    def test_login_com_credenciais_invalidas_permanece_na_pagina(self):
        response = self.client.post(
            reverse("login"), {"username": "joao", "password": "senhaErrada"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)


class DeslogarViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="senhaSegura123")

    def test_logout_encerra_sessao_e_redireciona_para_login(self):
        self.client.login(username="joao", password="senhaSegura123")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
