from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('formulario-material/', views.formulario_material, name='formulario_material'),
    path('gracias/', views.gracias, name='gracias'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logOut'),  
]
