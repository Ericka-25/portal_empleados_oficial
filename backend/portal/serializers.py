from rest_framework import serializers
from .models import User, Cliente, CotizacionHoras, Incidente, RegistroHoras

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'codigo_usuario', 'username', 'email', 'fecha_nacimiento', 'edad', 'rol', 'modulo']
        extra_kwargs = {'password': {'write_only': True}}

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CotizacionHorasSerializer(serializers.ModelSerializer):
    total_horas = serializers.SerializerMethodField()

    def get_total_horas(self, obj):
        return obj.horas_preanalisis + obj.horas_analisis + obj.horas_desarrollo + obj.horas_pruebas + obj.horas_documentacion

    class Meta:
        model = CotizacionHoras
        fields = '__all__'

class IncidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidente
        fields = '__all__'

class RegistroHorasSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroHoras
        fields = '__all__'