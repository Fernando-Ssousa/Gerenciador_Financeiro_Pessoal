from django.contrib import admin
from .models import Conta, Categoria, Transacao, MetaFinanceira, Parcela

admin.site.register(Conta)
admin.site.register(Categoria)
admin.site.register(Transacao)
admin.site.register(MetaFinanceira)
admin.site.register(Parcela)
