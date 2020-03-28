from django.urls import path
from . import views

# auth/...

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login-user"),
    path('signup/', views.SignUpView.as_view(), name="signup-user"),
    path('retrieve/', views.RetrieveUserView.as_view(), name="retrieve-user")
]
