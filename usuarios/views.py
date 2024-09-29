from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MaterialForm
from django.contrib.auth import logout



# Vista para el login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.rol == 'RECOLECTOR':
                return redirect('formulario_material')
            else:
                return redirect('home')
    return render(request, 'usuarios/login.html')

# Vista para el formulario del recolector
@login_required
def formulario_material(request):
    if request.user.rol != 'RECOLECTOR':
        return redirect('home')
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            # Lógica para procesar el formulario
            return redirect('gracias')
    else:
        form = MaterialForm()
    return render(request, 'usuarios/formulario_material.html', {'form': form})

def gracias(request):
    return render(request, 'usuarios/gracias.html')

def home(request):
    return render(request, 'usuarios/home.html')


def logout_view(request):
    logout(request)
    return render(request, 'usuarios/logout.html')
