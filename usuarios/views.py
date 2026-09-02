from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import View
from .forms import RegistroUsuarioForm

class RegistrarView(View):
    def get(self, request):
        form = RegistroUsuarioForm()
        return render(request, 'usuarios/registrar.html', {'form': form})
    
    def post(self, request):
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Faça login.")
            return redirect('login')
        return render(request, 'usuarios/registrar.html', {'form': form})

class LogarView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'usuarios/login.html', {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
        return render(request, 'usuarios/login.html', {'form': form})

class DeslogarView(View):
    def get(self, request):
        logout(request)
        return redirect('login')