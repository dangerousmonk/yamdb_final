from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register(
    r'users',
    views.UserViewSet,
)

urlpatterns = [
    path('v1/auth/token/', views.get_token, name='obtain-token'),
    path('v1/auth/email/', views.generate_code, name='email-verify'),
    path('v1/', include(router_v1.urls)),
]
