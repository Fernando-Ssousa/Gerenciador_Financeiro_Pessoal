from django.db import models
from django.contrib.auth.models import User


class Conta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="Usuário")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Saldo Inicial")
    banco = models.CharField(max_length=100, verbose_name="Banco")
    tipo = models.CharField(
        max_length=50,
        choices=[('corrente','Conta Corrente'), ('poupanca','Poupança')],
        verbose_name="Tipo"
    )

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="Usuário")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    tipo = models.CharField(
        max_length=10,
        choices=[('receita','Receita'), ('despesa','Despesa')],
        verbose_name="Tipo"
    )

    def __str__(self):
        return self.nome


class Parcela(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, verbose_name="Conta")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    data_vencimento = models.DateField(verbose_name="Vencimento")
    pago = models.BooleanField(default=False, verbose_name="Pago")

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"


class Transacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, verbose_name="Conta")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoria")
    parcela = models.ForeignKey(Parcela, on_delete=models.SET_NULL, verbose_name="Parcela", null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    descricao = models.TextField(verbose_name="Descrição")
    data = models.DateField(verbose_name="Data")

    def __str__(self):
        return f"{self.categoria} - R$ {self.valor}"


class MetaFinanceira(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    descricao = models.CharField(max_length=200, verbose_name="Descrição")
    valor_alvo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Alvo")
    valor_atual = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Atual")
    prazo = models.DateField(verbose_name="Prazo")

    def __str__(self):
        return self.descricao
