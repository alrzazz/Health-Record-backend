from account.permissions import IsDoctor, IsPatient
from .models import *
from .serializer import *
from rest_framework import viewsets, mixins, status, views, generics
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from .pagination import ItemlimitPgination
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

    def list_turn(self, request, doctor_pk=None):
        queryset = Turn.objects.all().filter(doctor_id=doctor_pk, accepted=False)
        serializer = TurnSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_turn(self, request, doctor_pk=None, turn_pk=None):
        queryset = get_object_or_404(
            Turn.objects.all().filter(doctor_id=doctor_pk, accepted=False), id=turn_pk)
        serializer = TurnSerializer(queryset)
        return Response(serializer.data)

    def accept_turn(self, request, doctor_pk=None, turn_pk=None):
        serializer = TurnActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = get_object_or_404(
            Turn.objects.all().filter(doctor_id=doctor_pk), id=turn_pk)

        if request.data["action"] == "accept":
            if instance.accepted:
                return Response(data={"message": "You can't perform this action."},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            instance.accepted = True
            instance.patient = Patient.objects.get(user_id=request.user.id)
            instance.save()

        if request.data["action"] == "reject":
            if not instance.accepted or instance.patient.user.id != request.user.id:
                return Response(data={"message": "You can't perform this action."},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            instance.accepted = False
            instance.patient = None
            instance.save()

        return Response(data={"message": "Your turn "+request.data["action"]+"ed successfully."},
                        status=status.HTTP_202_ACCEPTED)

    def get_own_turn(self, request):
        queryset = Turn.objects.all().filter(
            **request.data, patient__user_id=request.user.id)
        serializer = TurnSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_own_appointment(self, request):
        queryset = Appointment.objects.filter(
            turn__patient__user_id=request.user.id)
        serializer = AppointmentSerializerRecursive(queryset, many=True)
        return Response(serializer.data)
