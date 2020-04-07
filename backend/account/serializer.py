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
        extra_kwargs = {'password': {'write_only': True},
                        'role': {'read_only': True}}


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = "__all__"

    def create(self, validated_data):
        user_ins = User.objects.create_user(
            **dict(validated_data.pop("user"), role=1))
        doctor = Doctor.objects.create(user_id=user_ins.pk, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        if validated_data["user"]:
            new_user = dict(validated_data.pop("user"))
            old_user = User.objects.get(pk=instance.user_id)
            old_user.username = new_user.get(
                'username', old_user.username)
            old_user.email = new_user.get('email', old_user.email)
            old_user.save()
        instance.first_name = validated_data.get(
            "first_name", instance.first_name)
        instance.last_name = validated_data.get(
            "last_name", instance.last_name)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number)
        instance.address = validated_data.get("address", instance.address)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        user_ins = User.objects.create_user(
            **dict(validated_data.pop("user")), role=2)
        patient = Patient.objects.create(user_id=user_ins.pk, **validated_data)
        return patient

    def update(self, instance, validated_data):
        if validated_data["user"]:
            new_user = dict(validated_data.pop("user"))
            old_user = User.objects.get(pk=instance.user_id)
            old_user.username = new_user.get(
                'username', old_user.username)
            old_user.email = new_user.get('email', old_user.email)
            old_user.save()
        instance.first_name = validated_data.get(
            "first_name", instance.first_name)
        instance.last_name = validated_data.get(
            "last_name", instance.last_name)
        instance.mobile_number = validated_data.get(
            "mobile_number", instance.mobile_number)
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = "__all__"


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password1 = serializers.CharField(required=True)
    old_password2 = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["old_password1"] != data["old_password2"]:
            raise serializers.ValidationError(
                "confirmation password not match")
        return data
