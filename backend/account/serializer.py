from rest_framework import serializers
from .models import User, Patient, Doctor


class RetrieveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = "__all__"

    def create(self, validated_data):
        user_ins = User.objects.create_user(**dict(validated_data.pop("user")))
        doctor = Doctor.objects.create(user_id=user_ins.pk, **validated_data)
        return doctor


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        user_ins = User.objects.create_user(**dict(validated_data.pop("user")))
        patient = Patient.objects.create(user_id=user_ins.pk, **validated_data)
        return patient
