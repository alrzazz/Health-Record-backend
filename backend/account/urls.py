from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# auth/...

manage_router = DefaultRouter()
manage_router.register('doctor', views.ManageDoctorsView)
manage_router.register('patient', views.ManagePatientsView)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="login-user"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh-user"),
    path('retrieve/', views.RetrieveUserView.as_view(), name="retrieve-user"),
    path('profile/', views.ProfileView.as_view(), name="profile-user"),
    path('logout/', views.UserLogoutView.as_view(), name="logout-user"),
    path('change-password/', views.UserChangePasswordView.as_view(),
         name="logout-user"),
    path('manage/', include(manage_router.urls))
]
