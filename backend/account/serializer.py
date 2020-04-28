from rest_framework import serializers
from .models import User, Patient, Doctor


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True},
                        'role': {'read_only': True}}


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if len(data["new_password1"]) < 6:
            raise serializers.ValidationError(
                "This password is too short, your password at least 6 character"
            )
        if data["new_password1"] != data["new_password2"]:
            raise serializers.ValidationError(
                "confirmation password not match")
        return data
