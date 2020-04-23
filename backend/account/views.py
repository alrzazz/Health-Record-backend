from .permissions import IsManager, IsPatient, IsDoctor, NotManager
from .models import User, Doctor, Patient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions, exceptions
from rest_framework import permissions, generics, viewsets, views
from rest_framework.response import Response
from .serializer import *
import json


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
        serializer = RetrieveUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = [NotManager]

    def get(self, request):
        if request.user.role == 1:
            serializer = DoctorSerializer(
                Doctor.objects.all().get(user_id=request.user.id))
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        if request.user.role == 2:
            serializer = PatientSerializer(
                Patient.objects.all().get(user_id=request.user.id))
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        if request.user.role == 1:
            instance = Doctor.objects.all().get(user_id=request.user.id)
            serializer = DoctorSerializer(instance)
            serializer.update(instance, request.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        if request.user.role == 2:
            instance = Patient.objects.all().get(user_id=request.user.id)
            serializer = PatientSerializer(instance)
            serializer.update(instance, request.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        return self.put(request)


class ManageDoctorsView(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def update(self, request, pk=None):
        raise exceptions.MethodNotAllowed(request.method)


class ManagePatientsView(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def update(self, request, pk=None):
        raise exceptions.MethodNotAllowed(request.method)


class UserChangePasswordView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user_ins = User.objects.get(pk=request.user.id)
            if not user_ins.check_password(serializer.data.get("old_password1")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user_ins.set_password(serializer.data.get("new_password"))
            user_ins.save()

            return Response(data={'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.update(request)
