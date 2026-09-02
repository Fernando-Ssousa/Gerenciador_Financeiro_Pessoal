from django.urls import path
from .views import RegistrarView, LogarView, DeslogarView

urlpatterns = [
    path('registrar/', RegistrarView.as_view(), name='registrar'),
    path('', LogarView.as_view(), name='login'),
    path('logout/', DeslogarView.as_view(), name='logout'),
]