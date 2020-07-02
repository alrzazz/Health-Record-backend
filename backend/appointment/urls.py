from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, DynamicRoute

doctor_router = DefaultRouter()
doctor_router.register('advices', views.ManageAdviceView, basename='advices')
doctor_router.register('diseases', views.ManageDiseaseView, basename='diseases')
doctor_router.register('symptoms', views.ManageSymptomView, basename='symptoms')
doctor_router.register('medicines', views.ManageMedicineView, basename='medicines')
doctor_router.register('calendar', views.DoctorCalendarView, basename='calendars')
doctor_router.register('', views.DoctorAppointmentView, basename='appointments')

patient_router = DefaultRouter()
patient_router.register('turns', views.PatientListTurnView, basename='turns')
patient_router.register('', views.PatientAppointmentView, basename='appointments')

# appointment/...
urlpatterns = [
    path('doctor/', include((doctor_router.urls, "doctor"), namespace="doctor")),
    path('patient/', include((patient_router.urls, "patient"), namespace="patient")),
]
