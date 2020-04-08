from account.permissions import IsDoctor, IsPatient
from .models import *
from .serializer import *
from rest_framework import viewsets, mixins, status, views
from rest_framework.response import Response


class ManageSymptomView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = SymptomSerializer

    def get_queryset(self):
        return Symptom.objects.all().filter(
            doctor_id=self.request.user.id)


class ManageDiseaseView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = DiseaseSerializer

    def get_queryset(self):
        self.get_object
        return Disease.objects.all().filter(
            doctor_id=self.request.user.id)


class ManageAdviceView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = AdviceSerializer

    def get_queryset(self):
        return Advice.objects.all().filter(
            doctor_id=self.request.user.id)


class ManageMedicineView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = MedicineSerializer

    def get_queryset(self):
        return Medicine.objects.all().filter(
            doctor_id=self.request.user.id)


class DoctorTurnView(viewsets.ViewSet):
    permission_classes = [IsDoctor]

    def create_turn(self, request):
        serializer = TurnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        turn = Turn.objects.create(**serializer.data, doctor=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_turn(self, request, pk=None):
        instance = Turn.objects.get(id=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list_turn(self, request):
        queryset = Turn.objects.filter(**request.data, doctor=request.user.id)
        serializer = TurnSerializer(queryset, many=True)
        return Response(serializer.data)


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

    def select_doctor(self, request):
        if "doctor" in request.data:
            request.user.actions["doctor"] = request.data["doctor"]
            request.user.save()
            return Response(data={"message": "Doctor selected " + request.user.actions["doctor"] + " successfully"},
                            status=status.HTTP_200_OK)
        return Response(data={"message": "Doctor not selected"},
                        status=status.HTTP_400_BAD_REQUEST)

    def get_doctor(self, request):
        if "doctor" in request.user.actions:
            queryset = Doctor.objects.get(id=request.user.actions["doctor"])
            serializer = DoctorSerializer(queryset)
            return Response(serializer.data)
        return Response(data={"message": "Doctor not selected"},
                        status=status.HTTP_400_BAD_REQUEST)

    def list_turn(self, request):
        if "doctor" in request.user.actions:
            queryset = Turn.objects.filter(
                doctor_id=request.user.actions["doctor"]).filter(patient=None)
            serializer = TurnSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(data={"message": "Doctor not selected"},
                        status=status.HTTP_400_BAD_REQUEST)

    def select_turn(self, request):
        if "doctor" not in request.user.actions:
            return Response(data={"message": "Doctor not selected"},
                            status=status.HTTP_400_BAD_REQUEST)
        if "turn" not in request.data:
            return Response(data={"message": "Turn not selected"},
                            status=status.HTTP_400_BAD_REQUEST)
        request.user.actions["turn"] = request.data["turn"]
        request.user.save()
        return Response(data={"message": "Turn selected " + request.user.actions["turn"] + " successfully"},
                        status=status.HTTP_200_OK)

    def get_turn(self, request):
        if "doctor" not in request.user.actions:
            return Response(data={"message": "Doctor not selected"},
                            status=status.HTTP_400_BAD_REQUEST)
        if "turn" not in request.user.actions:
            return Response(data={"message": "Turn not selected"},
                            status=status.HTTP_400_BAD_REQUEST)
        queryset = Turn.objects.get(id=request.user.actions["turn"])
        serializer = TurnSerializer(queryset)
        return Response(serializer.data)

    def accept_turn(self, request):
        if "doctor" not in request.user.actions:
            return Response(data={"message": "Doctor not selected"},
                            status=status.HTTP_400_BAD_REQUEST)
        if "turn" not in request.user.actions:
            return Response(data={"message": "Turn not selected"},
                            status=status.HTTP_400_BAD_REQUEST)
        turn = Turn.objects.get(id=request.user.actions["turn"])
        turn.patient = request.user
        turn.accepted = True
        turn.save()
        request.user.actions = dict
        request.user.save()
        return Response(data={"message": "Selected successfully reserved"},
                        status=status.HTTP_200_OK)

    def get_own_turn(self, request):
        queryset = Turn.objects.all().filter(**request.data, patient_id=request.user.id)
        serializer = TurnSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_own_appointment(self, request):
        queryset = Appointment.objects.filter(turn__patient_id=request.user.id)
        serializer = AppointmentSerializerRecursive(queryset, many=True)
        return Response(serializer.data)
