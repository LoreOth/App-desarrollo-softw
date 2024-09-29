from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    RECOLECTOR = 'RECOLECTOR'
    ADMINISTRADOR = 'ADMINISTRADOR'
    
    ROLES = [
        (RECOLECTOR, 'Recolector'),
        (ADMINISTRADOR, 'Administrador'),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, default=RECOLECTOR)

    # Añadir el related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
