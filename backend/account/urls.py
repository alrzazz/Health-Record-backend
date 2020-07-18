from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

manager_router = DefaultRouter()
manager_router.register('doctors', views.ManageDoctorsView, basename="doctors")
manager_router.register('patients', views.ManagePatientsView, basename="patients")

# auth/...
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="login-user"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh-user"),
    path('retrieve/', views.RetrieveUserView.as_view(), name="retrieve-user"),
    path('profile/', views.ProfileView.as_view(), name="profile-user"),
    path('logout/', views.UserLogoutView.as_view(), name="logout-user"),
    path('change-password/', views.UserChangePasswordView.as_view(), name="change-password"),
    path('manager/', include((manager_router.urls, "manage"), namespace="manage"))
]
