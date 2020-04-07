from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter, DynamicRoute

# appointment/...

router = DefaultRouter()
router.register('advice', views.ManageAdviceView, basename='advice-view')
router.register('disease', views.ManageDiseaseView, basename='disease-view')
router.register('symptom', views.ManageSymptomView, basename='symptom-view')
router.register('medicine', views.ManageMedicineView, basename='medicine-view')

urlpatterns = [
    path('doctor/', include(router.urls)),
    path('doctor/turn/create/',
         views.DoctorTurnView.as_view({"post": "create_turn"})),
    path('doctor/turn/list/',
         views.DoctorTurnView.as_view({"post": "list_turn"})),
    path('doctor/turn/delete/<pk>/',
         views.DoctorTurnView.as_view({"delete": "delete_turn"})),
    path("patient/doctor/list/",
         views.PatientTurnView.as_view({"post": "list_doctor"})),
    path("patient/doctor/select/",
         views.PatientTurnView.as_view({"post": "select_doctor"})),
    path("patient/doctor/get/",
         views.PatientTurnView.as_view({"get": "get_doctor"})),
    path("patient/turn/list/",
         views.PatientTurnView.as_view({"get": "list_turn"})),
    path("patient/turn/select/",
         views.PatientTurnView.as_view({"post": "select_turn"})),
    path("patient/turn/accept/",
         views.PatientTurnView.as_view({"get": "get_turn",
                                        "post": "accept_turn"})),
    path("patient/turn/",
         views.PatientTurnView.as_view({"post": "get_own_turn"})),
]
