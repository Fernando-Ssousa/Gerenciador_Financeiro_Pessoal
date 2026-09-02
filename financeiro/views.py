from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, F
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views import View
from .models import Conta, Categoria, Parcela, Transacao, MetaFinanceira
from .forms import ContaForm, CategoriaForm, ParcelaForm, TransacaoForm, MetaFinanceiraForm

# Dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = '_layouts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        hoje = timezone.now()
        
        transacoes = Transacao.objects.filter(usuario=usuario)
        
        saldo_total = transacoes.aggregate(Sum('valor'))['valor__sum'] or 0
        
        receitas_mes = transacoes.filter(
            categoria__tipo='receita', 
            data__month=hoje.month, 
            data__year=hoje.year
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        
        despesas_mes = transacoes.filter(
            categoria__tipo='despesa', 
            data__month=hoje.month, 
            data__year=hoje.year
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        
        seis_meses_atras = hoje - timedelta(days=180)
        transacoes_ultimos_meses = transacoes.filter(data__gte=seis_meses_atras)
        
        meses_data = []
        receitas_data = []
        despesas_data = []
        
        for i in range(6):
            mes = hoje - timedelta(days=30*i)
            mes_nome = mes.strftime('%b/%Y')
            meses_data.append(mes_nome)
            
            receitas_mes_item = transacoes.filter(
                categoria__tipo='receita',
                data__month=mes.month,
                data__year=mes.year
            ).aggregate(Sum('valor'))['valor__sum'] or 0
            
            despesas_mes_item = transacoes.filter(
                categoria__tipo='despesa',
                data__month=mes.month,
                data__year=mes.year
            ).aggregate(Sum('valor'))['valor__sum'] or 0
            
            receitas_data.append(float(receitas_mes_item))
            despesas_data.append(float(despesas_mes_item))
        
        meses_data.reverse()
        receitas_data.reverse()
        despesas_data.reverse()
        
        categorias_gastos = transacoes.filter(
            categoria__tipo='despesa',
            data__month=hoje.month,
            data__year=hoje.year
        ).values('categoria__nome').annotate(total=Sum('valor')).order_by('-total')[:8]
        
        categorias_nomes = [item['categoria__nome'] for item in categorias_gastos]
        categorias_valores = [float(item['total'] or 0) for item in categorias_gastos]
        
        metas = MetaFinanceira.objects.filter(usuario=usuario)
        metas_concluidas = metas.filter(valor_atual__gte=F('valor_alvo')).count()
        metas_andamento = metas.filter(valor_atual__lt=F('valor_alvo')).count()
        
        context.update({
            'saldo_total': saldo_total,
            'receitas': receitas_mes,
            'despesas': despesas_mes,
            'meses_data': meses_data,
            'receitas_data': receitas_data,
            'despesas_data': despesas_data,
            'categorias_nomes': categorias_nomes,
            'categorias_valores': categorias_valores,
            'metas_concluidas': metas_concluidas,
            'metas_andamento': metas_andamento,
            'total_metas': metas.count(),
        })
        
        return context


# Conta
class ContaListView(LoginRequiredMixin, ListView):
    model = Conta
    template_name = 'financeiro/contas/contas_list.html'
    context_object_name = 'contas'
    paginate_by = 6

    def get_queryset(self):
        queryset = Conta.objects.filter(usuario=self.request.user).order_by('nome')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(nome__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class ContaCreateView(LoginRequiredMixin, CreateView):
    model = Conta
    form_class = ContaForm
    template_name = 'financeiro/contas/conta_form.html'
    success_url = reverse_lazy('contas_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class ContaUpdateView(LoginRequiredMixin, UpdateView):
    model = Conta
    form_class = ContaForm
    template_name = 'financeiro/contas/conta_form.html'
    success_url = reverse_lazy('contas_list')

    def get_queryset(self):
        return Conta.objects.filter(usuario=self.request.user)

class ContaDeleteView(LoginRequiredMixin, DeleteView):
    model = Conta
    template_name = 'financeiro/contas/conta_deletar.html'
    success_url = reverse_lazy('contas_list')

    def get_queryset(self):
        return Conta.objects.filter(usuario=self.request.user)


# Categoria
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'financeiro/categorias/categorias_list.html'
    context_object_name = 'categorias'
    paginate_by = 6

    def get_queryset(self):
        queryset = Categoria.objects.filter(usuario=self.request.user).order_by('nome')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(nome__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'financeiro/categorias/categoria_form.html'
    success_url = reverse_lazy('categorias_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'financeiro/categorias/categoria_form.html'
    success_url = reverse_lazy('categorias_list')

    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'financeiro/categorias/categoria_deletar.html'
    success_url = reverse_lazy('categorias_list')

    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)


# Parcela
class ParcelaListView(LoginRequiredMixin, ListView):
    model = Parcela
    template_name = 'financeiro/parcelas/parcelas_list.html'
    context_object_name = 'parcelas'
    paginate_by = 6

    def get_queryset(self):
        queryset = Parcela.objects.filter(usuario=self.request.user).order_by('data_vencimento')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(descricao__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class ParcelaCreateView(LoginRequiredMixin, CreateView):
    model = Parcela
    form_class = ParcelaForm
    template_name = 'financeiro/parcelas/parcela_form.html'
    success_url = reverse_lazy('parcelas_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class ParcelaUpdateView(LoginRequiredMixin, UpdateView):
    model = Parcela
    form_class = ParcelaForm
    template_name = 'financeiro/parcelas/parcela_form.html'
    success_url = reverse_lazy('parcelas_list')

    def get_queryset(self):
        return Parcela.objects.filter(usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ParcelaDeleteView(LoginRequiredMixin, DeleteView):
    model = Parcela
    template_name = 'financeiro/parcelas/parcela_deletar.html'
    success_url = reverse_lazy('parcelas_list')

    def get_queryset(self):
        return Parcela.objects.filter(usuario=self.request.user)


# Transação
class TransacaoListView(LoginRequiredMixin, ListView):
    model = Transacao
    template_name = 'financeiro/transacoes/transacoes_list.html'
    context_object_name = 'transacoes'
    paginate_by = 6

    def get_queryset(self):
        queryset = Transacao.objects.filter(usuario=self.request.user).order_by('-data')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(descricao__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context

class TransacaoCreateView(LoginRequiredMixin, CreateView):
    model = Transacao
    form_class = TransacaoForm
    template_name = 'financeiro/transacoes/transacao_form.html'
    success_url = reverse_lazy('transacoes_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class TransacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Transacao
    form_class = TransacaoForm
    template_name = 'financeiro/transacoes/transacao_form.html'
    success_url = reverse_lazy('transacoes_list')

    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class TransacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Transacao
    template_name = 'financeiro/transacoes/transacao_deletar.html'
    success_url = reverse_lazy('transacoes_list')

    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user)

class ParcelaDataView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        parcela = get_object_or_404(Parcela, pk=pk, usuario=request.user)
        data = {
            'conta': parcela.conta.id,
            'categoria': parcela.categoria.id,
            'valor': str(parcela.valor),
        }
        return JsonResponse(data)


# Meta
class MetaListView(LoginRequiredMixin, ListView):
    model = MetaFinanceira
    template_name = 'financeiro/metas/metas_list.html'
    context_object_name = 'metas'
    paginate_by = 6

    def get_queryset(self):
        queryset = MetaFinanceira.objects.filter(usuario=self.request.user)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(descricao__icontains=search)
            
        return queryset.order_by('prazo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['search'] = self.request.GET.get('search', '')
        
        metas = context['metas']
        for meta in metas:
            if meta.valor_alvo > 0:
                meta.progresso = (meta.valor_atual / meta.valor_alvo) * 100
            else:
                meta.progresso = 0

            if meta.progresso < 30:
                meta.cor = "bg-danger"
            elif meta.progresso < 70:
                meta.cor = "bg-warning"
            else:
                meta.cor = "bg-success"
                
        return context

class MetaCreateView(LoginRequiredMixin, CreateView):
    model = MetaFinanceira
    form_class = MetaFinanceiraForm
    template_name = 'financeiro/metas/meta_form.html'
    success_url = reverse_lazy('metas_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class MetaUpdateView(LoginRequiredMixin, UpdateView):
    model = MetaFinanceira
    form_class = MetaFinanceiraForm
    template_name = 'financeiro/metas/meta_form.html'
    success_url = reverse_lazy('metas_list')

    def get_queryset(self):
        return MetaFinanceira.objects.filter(usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class MetaDeleteView(LoginRequiredMixin, DeleteView):
    model = MetaFinanceira
    template_name = 'financeiro/metas/meta_deletar.html'
    success_url = reverse_lazy('metas_list')

    def get_queryset(self):
        return MetaFinanceira.objects.filter(usuario=self.request.user)
