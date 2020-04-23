from account.permissions import IsDoctor, IsPatient
from .models import *
from .serializer import *
from rest_framework import viewsets, mixins, status, views
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except:
        raise Http404


class ManageSymptomView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = SymptomSerializer

    def get_queryset(self):
        return Symptom.objects.all().filter(
            doctor__user_id=self.request.user.id)


class ManageDiseaseView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = DiseaseSerializer

    def get_queryset(self):
        self.get_object
        return Disease.objects.all().filter(
            doctor__user_id=self.request.user.id)


class ManageAdviceView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = AdviceSerializer

    def get_queryset(self):
        return Advice.objects.all().filter(
            doctor__user_id=self.request.user.id)


class ManageMedicineView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = MedicineSerializer

    def get_queryset(self):
        return Medicine.objects.all().filter(
            doctor__user_id=self.request.user.id)


class DoctorTurnView(mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsDoctor]
    serializer_class = TurnSerializer

    def get_queryset(self):
        return Turn.objects.all().filter(doctor__user_id=self.request.user.id)


class DoctorAppointment(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.all().filter(turn__doctor_id=self.request.user.id)


class PatientTurnView(viewsets.ViewSet):
    permission_classes = [IsPatient]

    def list_doctor(self, request):
        queryset = Doctor.objects.all().filter(**request.data)
        serializer = DoctorSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_doctor(self, request, doctor_pk=None):
        queryset = get_object_or_404(Doctor.objects.all(), id=doctor_pk)
        serializer = DoctorSerializer(queryset)
        return Response(serializer.data)

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
