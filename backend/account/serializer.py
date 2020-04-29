from rest_framework import serializers
from .models import User, Patient, Doctor


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
        user_request = validated_data.pop("user")
        user_request["role"] = 1
        user_srializer = UserSerializer(data=user_request)
        user_srializer.is_valid(raise_exception=True)
        user_instance = User.objects.create_user(**user_request)
        validated_data["user_id"] = user_instance.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "user" in validated_data:
            request_user = validated_data.pop("user")
            instance_user = instance.user
            serializer = UserSerializer(
                instance_user, data=request_user, partial=True)
            if(not serializer.is_valid()):
                raise serializers.ValidationError
            serializer.save()
        return super().update(instance, validated_data)


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        user_request = validated_data.pop("user")
        user_request["role"] = 1
        user_srializer = UserSerializer(data=user_request)
        user_srializer.is_valid(raise_exception=True)
        user_instance = User.objects.create_user(**user_request)
        validated_data["user_id"] = user_instance.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "user" in validated_data:
            request_user = validated_data.pop("user")
            instance_user = instance.user
            serializer = UserSerializer(
                instance_user, data=request_user, partial=True)
            if(not serializer.is_valid()):
                raise serializers.ValidationError
            serializer.save()
        return super().update(instance, validated_data)


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
