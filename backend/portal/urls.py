from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'clientes', views.ClienteViewSet)
router.register(r'cotizaciones', views.CotizacionHorasViewSet)
router.register(r'incidentes', views.IncidenteViewSet)
router.register(r'registro-horas', views.RegistroHorasViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]