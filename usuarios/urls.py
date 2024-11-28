from django.urls import path
from . import views
from .views import registro_view
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('formulario-material/', views.formulario_material, name='formulario_material'),
    path('reporte_meteriales/', views.reporte_meteriales, name='reporte_meteriales'),

    path('gracias/', views.gracias, name='gracias'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),

    path('logout/', views.logout_view, name='logOut'),  
    path('registro/', registro_view, name='registro'),
    path('aprobar-material/<int:material_id>/', views.aprobar_material, name='aprobar_material'),
    path('materiales/', views.MaterialesListView.as_view(), name='listar_materiales'),
    path('materiales/actualizar/', views.ActualizarCantidadMaterialView.as_view(), name='actualizar_material'),
    path('resumen-materiales-recicladores/', views.resumen_materiales_y_recicladores, name='resumen_materiales_recicladores'),
]
