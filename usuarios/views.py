from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import Material, MaterialForm, Materiales
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import MaterialForm
from django.contrib.auth.decorators import login_required, permission_required


from .models import Usuario  # Importar el modelo personalizado

from .functions.load_material import run_load_material

# Vista para el registro de usuarios
def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        last_name = request.POST['last_name']  # Recibir apellido
        email = request.POST['email']  # Recibir email
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        rol = request.POST['rol']
        
        # Validar que ambas contraseñas coincidan
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro')  # Redirigir al formulario de registro en caso de error
        
        # Validar que el email no esté ya registrado
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
            return redirect('registro')

        # Crear usuario y asignar los campos adicionales
        user = Usuario.objects.create(
            username=username,
            last_name=last_name,  # Guardar apellido
            email=email,  # Guardar email
            password=make_password(password),  # Encriptar la contraseña
            rol=rol  # Asignar el rol
        )
        
        # Iniciar sesión automáticamente después de registrar
        login(request, user)
        
        # Redireccionar dependiendo del rol
        if rol == 'RECOLECTOR':
            return redirect('formulario_material')
        else:
            return redirect('home')
    
    return render(request, 'usuarios/registro.html')

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


def formulario_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit = False)  # Usa save() aquí
            material.user = request.user  # Asegúrate de que el usuario esté asociado
            material.save()  # Guarda la instancia en la base de datos

            run_load_material(material.user_id, material.id)
            
            return redirect('home')  # Redirige a otra página después de guardar
    else:
        form = MaterialForm()

    return render(request, 'usuarios/formulario_material.html', {'form': form})


def gracias(request):
    return render(request, 'usuarios/gracias.html')

def home(request):
    # Si el usuario es un depósito, mostrar los materiales pendientes y aprobados
    if request.user.rol == 'DEPOSITO':
        # Obtener materiales que no han sido aprobados (supervisado=False)
        materiales_pendientes = Material.objects.filter(supervisado=False)
        
        # Obtener materiales que ya han sido aprobados (supervisado=True)
        materiales_aprobados = Material.objects.filter(supervisado=True)
        
        # Pasar estas listas al contexto de la plantilla
        return render(request, 'usuarios/home.html', {
            'materiales_pendientes': materiales_pendientes,
            'materiales_aprobados': materiales_aprobados,
        })
    
    # Si el usuario no es un depósito, simplemente renderizar la página
    return render(request, 'usuarios/home.html')


def logout_view(request):
    logout(request)
    return render(request, 'usuarios/logout.html')


@login_required
def aprobar_material(request, material_id):
    if request.method == 'POST':
        # Obtener el material usando get_object_or_404 para manejar errores si no existe
        material = get_object_or_404(Material, id=material_id)
        
        # Obtener la cantidad real ingresada en el formulario
        cantidad_real = request.POST.get('cantidad_real')
        
        if cantidad_real is not None:
            # Actualizar la cantidad real y marcar como supervisado
            material.cantidad_real = int(cantidad_real)
            material.supervisado = True  # Cambiar el flag de supervisado a True
            material.save()  # Guardar los cambios en la base de datos
        
        # Redirigir al home después de guardar los cambios
        return redirect('home')

    # Si no es un método POST, retornar un error 405
    return HttpResponse("Método no permitido", status=405)

