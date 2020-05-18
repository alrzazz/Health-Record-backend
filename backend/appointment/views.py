from account.permissions import IsDoctor, IsPatient
from .models import *
from .serializer import *
from rest_framework import viewsets, mixins, status, views, generics
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from .pagination import ItemlimitPgination
import datetime
from rest_framework.filters import SearchFilter, OrderingFilter


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except:
        raise Http404


class ManageSymptomView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = SymptomSerializer
    pagination_class = ItemlimitPgination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        return Symptom.objects.all().filter(
            doctor__user_id=self.request.user.id)


class ManageDiseaseView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = DiseaseSerializer
    pagination_class = ItemlimitPgination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        self.get_object
        return Disease.objects.all().filter(
            doctor__user_id=self.request.user.id)


class ManageAdviceView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = AdviceSerializer
    pagination_class = ItemlimitPgination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        return Advice.objects.all().filter(
            doctor__user_id=self.request.user.id)


class ManageMedicineView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = MedicineSerializer
    pagination_class = ItemlimitPgination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        return Medicine.objects.all().filter(
            doctor__user_id=self.request.user.id)


class DoctorCalendarView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = CalendarSerializer
    pagination_class = ItemlimitPgination
    filter_backends = [OrderingFilter]
    ordering_fields = ["day", "start_time"]
    queryset = Calendar.objects.all()

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(doctor__user_id=self.request.user.id)

        start = self.request.query_params.get("start")
        queryset = queryset.filter(
            day__gte=start) if start != None else queryset

        end = self.request.query_params.get("end")
        queryset = queryset.filter(day__lte=end) if end != None else queryset

        return queryset


class DoctorAppointmentView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.all().filter(doctor__user_id=self.request.user.id)


class PatientListTurnView(viewsets.ModelViewSet):
    permission_classes = [IsPatient]
    pagination_class = ItemlimitPgination
    serializer_class = PatientCalendarSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["doctor__first_name",
                     "doctor__last_name", "doctor__speciality"]
    ordering_fields = ["day", "start_time"]
    queryset = Calendar.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            day__gte=datetime.date.today() + datetime.timedelta(days=1), remained__gt=0)

        start = self.request.query_params.get("start")
        queryset = queryset.filter(
            day__gte=start) if start != None else queryset

        end = self.request.query_params.get("end")
        queryset = queryset.filter(day__lte=end) if end != None else queryset

        return queryset

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        serializer = TurnReserveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = request.data.get("action")
        calendar_id = request.data.get("calendar_id")
        print(action)
        if action == "accept":
            calendar = get_object_or_404(self.get_queryset(), id=calendar_id)
            turn = calendar.total - calendar.remained + 1
            patient = Patient.objects.get(user__id=self.request.user.id)
            Appointment.objects.create(
                calendar=calendar, turn=turn, patient=patient)
            calendar.remained -= 1
            calendar.save()
            return Response(data={"message": "Your Turn reserved"}, status=status.HTTP_200_OK)
        return Response(data={"message": "Turn not reserved"}, status=status.HTTP_400_BAD_REQUEST)
