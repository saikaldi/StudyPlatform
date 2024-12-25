from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_ratelimit.decorators import ratelimit
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profile', ProfileViewSet, basename='Profile')
urlpatterns = [
    path('sign-up/', RegisterView.as_view(), name='register'),
    path('sign-up-confirmation/', ConfirmRegistrationView.as_view(), name='sign-up-confirmation'),
    path('sign-in/', LoginView.as_view(), name='sign-in'),
    
    path('confirm-user-status-priveligion/', AdminConfirmUserView.as_view(), name='confirm-user'),

    path('request-password-reset/', ratelimit(key='ip', rate='1/10m', method='POST', block=False)(RequestPasswordResetView.as_view()), name='request-password-reset'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/', include(router.urls))
]
