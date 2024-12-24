from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Cliente, CotizacionHoras, Incidente, RegistroHoras
from .serializers import (UserSerializer, ClienteSerializer,
                       CotizacionHorasSerializer, IncidenteSerializer,
                       RegistroHorasSerializer)
import datetime

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        modulo = self.request.query_params.get('modulo')
        rol = self.request.query_params.get('rol')
        if modulo:
            queryset = queryset.filter(modulo=modulo)
        if rol:
            queryset = queryset.filter(rol=rol)
        return queryset

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

class CotizacionHorasViewSet(viewsets.ModelViewSet):
    queryset = CotizacionHoras.objects.all()
    serializer_class = CotizacionHorasSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def total_horas(self, request, pk=None):
        cotizacion = self.get_object()
        total = (cotizacion.horas_preanalisis + cotizacion.horas_analisis +
                cotizacion.horas_desarrollo + cotizacion.horas_pruebas +
                cotizacion.horas_documentacion)
        return Response({'total_horas': total})

class IncidenteViewSet(viewsets.ModelViewSet):
    queryset = Incidente.objects.all()
    serializer_class = IncidenteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        incidente = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado in ['PENDIENTE', 'EN_PROGRESO', 'COMPLETADO']:
            incidente.estado = nuevo_estado
            incidente.save()
            return Response({'status': 'estado actualizado'})
        return Response({'error': 'Estado inválido'}, 
                       status=status.HTTP_400_BAD_REQUEST)

class RegistroHorasViewSet(viewsets.ModelViewSet):
    queryset = RegistroHoras.objects.all()
    serializer_class = RegistroHorasSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = RegistroHoras.objects.all()
        consultor_id = self.request.query_params.get('consultor')
        fecha_inicio = self.request.query_params.get('fecha_inicio')
        fecha_fin = self.request.query_params.get('fecha_fin')

        if consultor_id:
            queryset = queryset.filter(consultor_id=consultor_id)
        if fecha_inicio:
            queryset = queryset.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha__lte=fecha_fin)
        return queryset

    @action(detail=False, methods=['get'])
    def reporte_mensual(self, request):
        consultor_id = request.query_params.get('consultor')
        mes = request.query_params.get('mes')
        año = request.query_params.get('año')

        if not all([consultor_id, mes, año]):
            return Response({'error': 'Faltan parámetros requeridos'},
                          status=status.HTTP_400_BAD_REQUEST)

        fecha_inicio = datetime.date(int(año), int(mes), 1)
        if int(mes) == 12:
            fecha_fin = datetime.date(int(año) + 1, 1, 1)
        else:
            fecha_fin = datetime.date(int(año), int(mes) + 1, 1)

        registros = RegistroHoras.objects.filter(
            consultor_id=consultor_id,
            fecha__gte=fecha_inicio,
            fecha__lt=fecha_fin
        )

        return Response({
            'consultor': consultor_id,
            'mes': mes,
            'año': año,
            'registros': RegistroHorasSerializer(registros, many=True).data,
            'total_horas': sum(r.horas for r in registros)
        })