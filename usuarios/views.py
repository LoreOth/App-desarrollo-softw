from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from usuarios.serializers import MaterialesSerializer
from .forms import Material, MaterialForm, Materiales
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .forms import MaterialForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum, F
from .models import Usuario  # Importar el modelo personalizado
from .functions.load_material import recoleccion_materiales, validar_materiales
from django.utils.timezone import now, timedelta
from django.db.models import Avg, Count, F, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
            
            case_id = recoleccion_materiales(material.user.email, material.material)  
            material.bonita_task = case_id
            material.save()  # Guarda la instancia en la base de datos
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
            es_cantidad_real = 'true' if material.cantidad_real == material.cantidad else 'false'
            validar_materiales(material.bonita_task, es_cantidad_real)  

        # Redirigir al home después de guardar los cambios
        return redirect('home')

    # Si no es un método POST, retornar un error 405
    return HttpResponse("Método no permitido", status=405)




@login_required
def reporte_meteriales(request):
    if request.user.rol != 'RECOLECTOR':
        return HttpResponse("No autorizado", status=403)

    # Calcular el rango de fechas de las últimas 2 semanas
    #fecha_limite = now() - timedelta(weeks=2)

    # Filtrar materiales recolectados en las últimas 2 semanas
    materiales = Material.objects

    # Métricas
    cantidad_recolecciones = materiales.count()
    recolecciones_modificadas = materiales.filter(cantidad_real__isnull=False).count()
    porcentaje_modificadas = (recolecciones_modificadas / cantidad_recolecciones) * 100 if cantidad_recolecciones > 0 else 0
    promedio_por_material = materiales.values('material').annotate(promedio=Avg('cantidad'))

    contexto = {
        'cantidad_recolecciones': cantidad_recolecciones,
        'porcentaje_modificadas': porcentaje_modificadas,
        'promedio_por_material': promedio_por_material,
    }
    return render(request, 'usuarios/reporte_meteriales.html', contexto)

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

class MaterialesListView(APIView):
    """
    Vista para devolver todos los materiales.
    """
    def get(self, request):
        materiales = Materiales.objects.all()
        serializer = MaterialesSerializer(materiales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ActualizarCantidadMaterialView(APIView):
    """
    Vista para actualizar la cantidad total de un material, restando una cantidad específica.
    """

    def post(self, request):
        # Obtener el nombre y la cantidad a restar del cuerpo de la solicitud
        nombre = request.data.get('nombre')
        cantidad = request.data.get('cantidad')

        if not nombre or cantidad is None:
            return Response({
                "error": "Se requieren los campos 'nombre' y 'cantidad'"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            cantidad = int(cantidad)
            if cantidad < 0:
                raise ValueError("La cantidad a restar no puede ser negativa.")
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Buscar el material por nombre
        try:
            material = Materiales.objects.get(nombre=nombre)
        except Materiales.DoesNotExist:
            return Response({"error": "Material no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Restar la cantidad
        nueva_cantidad = material.cantidad_total - cantidad
        if nueva_cantidad < 0:
            return Response({"error": "La cantidad no puede ser menor a 0"}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar la cantidad y guardar el material
        material.cantidad_total = nueva_cantidad
        material.save()

        return Response({
            "success": "Cantidad total actualizada con éxito",
            "data": {"nombre": material.nombre, "cantidad_total": material.cantidad_total}
        }, status=status.HTTP_200_OK)
        
from django.db.models import Subquery, OuterRef
@login_required
def resumen_materiales_y_recicladores(request):
    # Obtener el resumen de materiales con cantidad total y costo unitario
    materiales_resumen = Materiales.objects.all()

    # Obtener los recicladores, su monto total y el material más recolectado
    recicladores_resumen = Material.objects.values('user', 'material') \
        .annotate(
            # Usamos Subquery para obtener el costo unitario de Materiales
            total_monto=Sum(F('cantidad_real') * Subquery(
                Materiales.objects.filter(nombre=OuterRef('material')).values('costo_unitario')[:1]
            )),
            material_mas_recolectado=Sum('cantidad_real')
        ).order_by('user')

    # Obtener el material más recolectado por cada reciclador
    recicladores_mas_recolectado = []
    for reciclador in recicladores_resumen:
        material_recolectado = Material.objects.filter(user=reciclador['user']) \
            .order_by('-cantidad_real').first()

        recicladores_mas_recolectado.append({
            'user': Usuario.objects.get(id=reciclador['user']),
            'material_mas_recolectado': material_recolectado.material if material_recolectado else 'N/A',
            'total_monto': reciclador['total_monto']
        })

    # Pasar toda la información al contexto para el template
    context = {
        'materiales_resumen': materiales_resumen,
        'recicladores_resumen': recicladores_mas_recolectado
    }

    return render(request, 'usuarios/resumen_materiales_recicladores.html', context)