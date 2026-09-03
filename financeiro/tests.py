import json
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Conta, MetaFinanceira, Parcela, Transacao


class ModelStrTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="senha123")

    def test_conta_str_retorna_nome(self):
        conta = Conta.objects.create(
            usuario=self.user, nome="Carteira", saldo_inicial=100, banco="Caixa", tipo="corrente"
        )
        self.assertEqual(str(conta), "Carteira")

    def test_categoria_str_retorna_nome(self):
        categoria = Categoria.objects.create(usuario=self.user, nome="Salário", tipo="receita")
        self.assertEqual(str(categoria), "Salário")

    def test_parcela_str_contem_descricao_e_valor(self):
        conta = Conta.objects.create(
            usuario=self.user, nome="Carteira", saldo_inicial=100, banco="Caixa", tipo="corrente"
        )
        categoria = Categoria.objects.create(usuario=self.user, nome="Mercado", tipo="despesa")
        parcela = Parcela.objects.create(
            usuario=self.user,
            conta=conta,
            categoria=categoria,
            descricao="Compra do mês",
            valor=250,
            data_vencimento=date(2026, 1, 10),
        )
        self.assertEqual(str(parcela), "Compra do mês - R$ 250")

    def test_meta_financeira_str_retorna_descricao(self):
        meta = MetaFinanceira.objects.create(
            usuario=self.user,
            descricao="Viagem",
            valor_alvo=5000,
            valor_atual=1000,
            prazo=date(2026, 12, 31),
        )
        self.assertEqual(str(meta), "Viagem")


class ContaViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="senha123")
        self.outro_user = User.objects.create_user(username="maria", password="senha123")

    def test_lista_contas_exige_login(self):
        response = self.client.get(reverse("contas_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_lista_contas_mostra_apenas_contas_do_usuario_logado(self):
        Conta.objects.create(
            usuario=self.user, nome="Minha Conta", saldo_inicial=100, banco="Nubank", tipo="corrente"
        )
        Conta.objects.create(
            usuario=self.outro_user, nome="Conta da Maria", saldo_inicial=50, banco="Itaú", tipo="poupanca"
        )

        self.client.login(username="joao", password="senha123")
        response = self.client.get(reverse("contas_list"))

        self.assertEqual(response.status_code, 200)
        contas = list(response.context["contas"])
        self.assertEqual(contas, [Conta.objects.get(nome="Minha Conta")])

    def test_criar_conta_associa_usuario_logado(self):
        self.client.login(username="joao", password="senha123")
        response = self.client.post(
            reverse("criar_conta"),
            {"nome": "Nova Conta", "saldo_inicial": "500.00", "banco": "Bradesco", "tipo": "corrente"},
        )
        self.assertRedirects(response, reverse("contas_list"))
        conta = Conta.objects.get(nome="Nova Conta")
        self.assertEqual(conta.usuario, self.user)

    def test_nao_pode_editar_conta_de_outro_usuario(self):
        conta_outro = Conta.objects.create(
            usuario=self.outro_user, nome="Conta da Maria", saldo_inicial=50, banco="Itaú", tipo="poupanca"
        )
        self.client.login(username="joao", password="senha123")
        response = self.client.get(reverse("editar_conta", args=[conta_outro.pk]))
        self.assertEqual(response.status_code, 404)

    def test_deletar_conta_propria(self):
        conta = Conta.objects.create(
            usuario=self.user, nome="Conta a excluir", saldo_inicial=10, banco="Caixa", tipo="corrente"
        )
        self.client.login(username="joao", password="senha123")
        response = self.client.post(reverse("deletar_conta", args=[conta.pk]))
        self.assertRedirects(response, reverse("contas_list"))
        self.assertFalse(Conta.objects.filter(pk=conta.pk).exists())


class ParcelaDataViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="senha123")
        self.outro_user = User.objects.create_user(username="maria", password="senha123")
        self.conta = Conta.objects.create(
            usuario=self.user, nome="Carteira", saldo_inicial=100, banco="Caixa", tipo="corrente"
        )
        self.categoria = Categoria.objects.create(usuario=self.user, nome="Mercado", tipo="despesa")
        self.parcela = Parcela.objects.create(
            usuario=self.user,
            conta=self.conta,
            categoria=self.categoria,
            descricao="Compra do mês",
            valor=250,
            data_vencimento=date(2026, 1, 10),
        )

    def test_retorna_dados_da_parcela_em_json(self):
        self.client.login(username="joao", password="senha123")
        response = self.client.get(reverse("parcela_data", args=[self.parcela.pk]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["conta"], self.conta.id)
        self.assertEqual(data["categoria"], self.categoria.id)
        self.assertEqual(data["valor"], "250.00")

    def test_retorna_404_para_parcela_de_outro_usuario(self):
        self.client.login(username="maria", password="senha123")
        response = self.client.get(reverse("parcela_data", args=[self.parcela.pk]))
        self.assertEqual(response.status_code, 404)


class TransacaoViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="senha123")
        self.conta = Conta.objects.create(
            usuario=self.user, nome="Carteira", saldo_inicial=100, banco="Caixa", tipo="corrente"
        )
        self.categoria = Categoria.objects.create(usuario=self.user, nome="Salário", tipo="receita")

    def test_criar_transacao_associa_usuario_logado(self):
        self.client.login(username="joao", password="senha123")
        response = self.client.post(
            reverse("criar_transacao"),
            {
                "conta": self.conta.id,
                "categoria": self.categoria.id,
                "valor": "1500.00",
                "descricao": "Salário de janeiro",
                "data": "2026-01-05",
            },
        )
        self.assertRedirects(response, reverse("transacoes_list"))
        transacao = Transacao.objects.get(descricao="Salário de janeiro")
        self.assertEqual(transacao.usuario, self.user)


class DashboardViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="senha123")

    def test_dashboard_exige_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_acessivel_para_usuario_logado(self):
        self.client.login(username="joao", password="senha123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("saldo_total", response.context)


class MetaFinanceiraViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joao", password="senha123")

    def test_lista_metas_calcula_progresso(self):
        MetaFinanceira.objects.create(
            usuario=self.user,
            descricao="Reserva de emergência",
            valor_alvo=1000,
            valor_atual=500,
            prazo=date(2026, 6, 1),
        )
        self.client.login(username="joao", password="senha123")
        response = self.client.get(reverse("metas_list"))

        self.assertEqual(response.status_code, 200)
        meta = response.context["metas"][0]
        self.assertEqual(meta.progresso, 50)
        self.assertEqual(meta.cor, "bg-warning")
