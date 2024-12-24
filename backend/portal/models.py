from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('PROG', 'Programador'),
        ('FUNC', 'Funcional'),
        ('HIBR', 'Híbrido'),
    ]
    
    MODULE_CHOICES = [
        ('ABAP', 'ABAP'),
        ('ABAP_CLOUD', 'ABAP Cloud'),
        ('FIORI', 'Fiori'),
        ('SD', 'SD'),
        ('MM', 'MM'),
        ('FI', 'FI'),
        ('CO', 'CO'),
        ('PS', 'PS'),
        ('PM', 'PM'),
        ('SAC', 'SAC'),
        ('SF', 'SF'),
        ('ARJBA', 'ARJBA'),
        ('BASIS', 'BASIS'),
    ]

    codigo_usuario = models.CharField(max_length=10, unique=True)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    rol = models.CharField(max_length=4, choices=ROLE_CHOICES)
    modulo = models.CharField(max_length=10, choices=MODULE_CHOICES)

class Cliente(models.Model):
    codigo_cliente = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    requisitos = models.TextField(blank=True)

class CotizacionHoras(models.Model):
    codigo_cotizacion = models.CharField(max_length=10, unique=True)
    tipo_consultor = models.CharField(max_length=4, choices=[('PROG', 'Programador'), ('FUNC', 'Funcional')])
    horas_preanalisis = models.IntegerField(default=0)
    horas_analisis = models.IntegerField(default=0)
    horas_desarrollo = models.IntegerField(default=0)
    horas_pruebas = models.IntegerField(default=0)
    horas_documentacion = models.IntegerField(default=0)

class Incidente(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=3, choices=[('INC', 'Incidente'), ('REQ', 'Requerimiento')])
    consultor_programador = models.ForeignKey(User, on_delete=models.PROTECT, related_name='incidentes_programador')
    consultor_funcional = models.ForeignKey(User, on_delete=models.PROTECT, related_name='incidentes_funcional')
    tiempo_asignado_programador = models.IntegerField()
    tiempo_asignado_funcional = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=[('PENDIENTE', 'Pendiente'), ('EN_PROGRESO', 'En Progreso'), ('COMPLETADO', 'Completado')], default='PENDIENTE')

class RegistroHoras(models.Model):
    consultor = models.ForeignKey(User, on_delete=models.CASCADE)
    incidente = models.ForeignKey(Incidente, on_delete=models.CASCADE)
    fecha = models.DateField()
    horas = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])