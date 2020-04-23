from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, DynamicRoute

# appointment/...

doctor_router = DefaultRouter()
doctor_router.register('advices', views.ManageAdviceView, basename='advice')
doctor_router.register('diseases', views.ManageDiseaseView, basename='disease')
doctor_router.register('symptoms', views.ManageSymptomView, basename='symptom')
doctor_router.register(
    'medicines', views.ManageMedicineView, basename='medicine')
doctor_router.register('turns', views.DoctorTurnView, basename='turn-doctor')
# doctor_router.register('', views.DoctorAppointment,basename='appointment-doctor')
urlpatterns = [
    path('doctor/', include(doctor_router.urls)),
    path("patient/doctors/",
         views.PatientTurnView.as_view({"post": "list_doctor"})),
    path("patient/doctors/<doctor_pk>/",
         views.PatientTurnView.as_view({"get": "get_doctor"})),
    path("patient/doctors/<doctor_pk>/turns/",
         views.PatientTurnView.as_view({"get": "list_turn"})),
    path("patient/doctors/<doctor_pk>/turns/<turn_pk>/",
         views.PatientTurnView.as_view({"get": "get_turn", "post": "accept_turn"})),
    path("patient/turns/",
         views.PatientTurnView.as_view({"post": "get_own_turn"})),
    path("patient/",
         views.PatientTurnView.as_view({"get": "get_own_appointment"}))
]
