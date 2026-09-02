from django import forms
from .models import Conta, Categoria, MetaFinanceira, Transacao, Parcela

class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = ['nome', 'saldo_inicial', 'banco', 'tipo']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo']

class ParcelaForm(forms.ModelForm):
    class Meta:
        model = Parcela
        fields = ['conta', 'categoria', 'descricao', 'valor', 'data_vencimento', 'pago']
        widgets = {
            'data_vencimento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['conta'].queryset = Conta.objects.filter(usuario=self.user)
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.user)
        
        if self.instance and self.instance.pk:
            self.fields['data_vencimento'].initial = self.instance.data_vencimento

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['parcela', 'conta', 'categoria', 'valor', 'descricao', 'data']
        widgets = {
            'data': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            )
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['parcela'].queryset = Parcela.objects.filter(usuario=self.user, pago=False)
            self.fields['conta'].queryset = Conta.objects.filter(usuario=self.user)
            self.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.user)
        
        if self.instance and self.instance.pk:
            self.fields['data'].initial = self.instance.data
        if self.instance and self.instance.pk and self.instance.parcela:
            self.fields['conta'].initial = self.instance.parcela.conta
            self.fields['categoria'].initial = self.instance.parcela.categoria
            self.fields['valor'].initial = self.instance.parcela.valor

class MetaFinanceiraForm(forms.ModelForm):
    class Meta:
        model = MetaFinanceira
        fields = ['descricao', 'valor_alvo', 'valor_atual', 'prazo']
        widgets = {
            'prazo': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk:
            self.fields['prazo'].initial = self.instance.prazo
