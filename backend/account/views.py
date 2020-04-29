from .permissions import IsManager, IsPatient, IsDoctor, NotManager
from .models import User, Doctor, Patient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions, exceptions
from rest_framework import permissions, generics, viewsets, views
from rest_framework.response import Response
from .serializer import *
import json
from .pagination import ItemlimitPgination


class UserLogoutView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format='json'):
        token = RefreshToken(request.data.get("refresh"))
        token.blacklist()
        data = {'message': "Logged out successfully"}
        return Response(data=data, status=status.HTTP_200_OK)


class RetrieveUserView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format='json'):
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [NotManager]

    def get_serializer_class(self):
        return DoctorSerializer if self.request.user.role == 1 else PatientSerializer

    def get_object(self):
        if self.request.user.role == 1:
            return Doctor.objects.get(user_id=self.request.user.id)
        return Patient.objects.get(user_id=self.request.user.id)


class ManageDoctorsView(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    pagination_class = ItemlimitPgination


class ManagePatientsView(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    pagination_class = ItemlimitPgination


class UserChangePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_ins = request.user
            if not user_ins.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user_ins.set_password(serializer.data.get("new_password1"))
            user_ins.save()

            return Response(data={'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.update(request)
