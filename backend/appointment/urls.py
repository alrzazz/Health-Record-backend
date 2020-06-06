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
doctor_router.register('calendar', views.DoctorCalendarView,
                       basename='calendar-doctor')
doctor_router.register('', views.DoctorAppointmentView,
                       basename='appointment-doctor')

patient_router = DefaultRouter()
patient_router.register('turns', views.PatientListTurnView, basename='turns')
patient_router.register(
    '', views.PatientAppointmentView, basename='appointment-patient')

urlpatterns = [
    path('doctor/', include(doctor_router.urls)),
    path('patient/', include(patient_router.urls)),
]
