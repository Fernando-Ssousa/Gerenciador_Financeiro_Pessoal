from django.urls import path
from .views import ContaListView, ContaCreateView, ContaUpdateView, ContaDeleteView
from .views import CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView
from .views import  TransacaoListView, TransacaoCreateView, TransacaoUpdateView, TransacaoDeleteView, ParcelaDataView
from .views import ParcelaListView, ParcelaCreateView, ParcelaUpdateView, ParcelaDeleteView
from .views import MetaListView, MetaCreateView, MetaUpdateView, MetaDeleteView
from .views import DashboardView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('contas/', ContaListView.as_view(), name='contas_list'),
    path('contas/nova/', ContaCreateView.as_view(), name='criar_conta'),
    path('contas/editar/<int:pk>/', ContaUpdateView.as_view(), name='editar_conta'),
    path('contas/deletar/<int:pk>/', ContaDeleteView.as_view(), name='deletar_conta'),

    path('categorias/', CategoriaListView.as_view(), name='categorias_list'),
    path('categorias/nova/', CategoriaCreateView.as_view(), name='criar_categoria'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('categorias/<int:pk>/deletar/', CategoriaDeleteView.as_view(), name='deletar_categoria'),

    path('parcelas/', ParcelaListView.as_view(), name='parcelas_list'),
    path('parcelas/nova/', ParcelaCreateView.as_view(), name='criar_parcela'),
    path('parcelas/editar/<int:pk>/', ParcelaUpdateView.as_view(), name='editar_parcela'),
    path('parcelas/deletar/<int:pk>/', ParcelaDeleteView.as_view(), name='deletar_parcela'),

    path('transacoes/', TransacaoListView.as_view(), name='transacoes_list'),
    path('transacoes/nova/', TransacaoCreateView.as_view(), name='criar_transacao'),
    path('transacoes/editar/<int:pk>/', TransacaoUpdateView.as_view(), name='editar_transacao'),
    path('transacoes/deletar/<int:pk>/', TransacaoDeleteView.as_view(), name='deletar_transacao'),
    path('api/parcela/<int:pk>/', ParcelaDataView.as_view(), name='parcela_data'),

    path('metas/', MetaListView.as_view(), name='metas_list'),
    path('metas/criar/', MetaCreateView.as_view(), name='criar_meta'),
    path('metas/editar/<int:pk>/', MetaUpdateView.as_view(), name='editar_meta'),
    path('metas/deletar/<int:pk>/', MetaDeleteView.as_view(), name='deletar_meta'),
    

]
