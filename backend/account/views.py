from rest_framework import permissions, generics, viewsets
from rest_framework.response import Response
from .serializer import RetrieveUserSerializer, DoctorSerializer, PatientSerializer
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Doctor, Patient
from .permissions import IsManager, IsPatient, IsDoctor, NotManager


class UserLogoutView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        token = RefreshToken(request.data.get("refresh"))
        token.blacklist()
        data = {'message': "خروج شما با موفقیت انجام شد."}
        return Response(data=data, status=status.HTTP_200_OK)


class RetrieveUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format='json'):
        serializer = RetrieveUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProfileUserView(generics.RetrieveAPIView):
    permission_classes = [NotManager]

    def get(self, request, format='json'):
        try:
            if(request.user.role == 1):
                serializer = DoctorSerializer(
                    Doctor.objects.get(user_id=request.user.id))
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = PatientSerializer(
                    Patient.objects.get(user_id=request.user.id))
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data={"message": "user not found"}, status=status.HTTP_403_FORBIDDEN)


class ManageDoctorsView(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class ManagePatientsView(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
