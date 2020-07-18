from rest_framework import serializers
from .models import Calendar, Symptom, Disease, Advice, Medicine, Appointment
from account.models import Doctor, Patient
from account.serializer import DoctorSerializer, PatientSerializer
import datetime


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ["id", "name", "value"]
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        doctor = Doctor.objects.get(
            user_id=self.context['request'].user.id)
        validated_data["doctor_id"] = doctor.id
        return super().create(validated_data)


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = ["id", "name"]
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        doctor = Doctor.objects.get(user_id=self.context['request'].user.id)
        validated_data["doctor_id"] = doctor.id
        return super().create(validated_data)


class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = ["id", "name", "description"]
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        doctor = Doctor.objects.get(user_id=self.context['request'].user.id)
        validated_data["doctor_id"] = doctor.id
        return super().create(validated_data)


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["id", "name", "duration"]
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        doctor = Doctor.objects.get(user_id=self.context['request'].user.id)
        validated_data["doctor_id"] = doctor.id
        return super().create(validated_data)


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ["id", "day", "start_time", "remained", "total"]
        extra_kwargs = {
            'remained': {'read_only': True}
        }

    def create(self, validated_data):
        doctor = Doctor.objects.get(user_id=self.context['request'].user.id)
        validated_data["doctor_id"] = doctor.id
        validated_data["remained"] = validated_data["total"]
        return super().create(validated_data)

    def validate(self, data):
        if data["day"] < datetime.date.today() + datetime.timedelta(days=1):
            raise serializers.ValidationError(
                "You can make turn at least for next 24 hours from now.")
        if data["day"] > datetime.date.today() + datetime.timedelta(weeks=3):
            raise serializers.ValidationError(
                "You can't make turn for after next 3 weeks in future.")
        return data


class DoctorField(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["first_name", "last_name", "speciality", "id", "gender"]


class PatientCalendarSerializer(serializers.ModelSerializer):
    doctor = DoctorField()

    class Meta:
        model = Calendar
        fields = ["id", "day", "start_time", "remained", "doctor"]


class PatientCalendarSerializerDetails(serializers.Serializer):
    doctor = DoctorSerializer()
    start_time = serializers.DateField()
    day = serializers.TimeField()
    time = serializers.DateField()
    remained = serializers.IntegerField()
    total = serializers.IntegerField()


class PatientField(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "id"]


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientField()
    calendar = CalendarSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"
        extra_kwargs = {
            'patient': {'read_only': True},
            'turn': {'read_only': True},
            'calendar': {'read_only': True}
        }


class AppointmentReadonlySerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    advices = AdviceSerializer(many=True)
    symptoms = SymptomSerializer(many=True)
    medicines = MedicineSerializer(many=True)
    disease = DiseaseSerializer(many=True)
    calendar = PatientCalendarSerializer()

    class Meta:
        model = Appointment
        fields = "__all__"
        depth = 2


class TurnReserveSerializer(serializers.Serializer):
    action = serializers.ChoiceField(
        choices=["accept", "reject", "status"], required=True)
    calendar_id = serializers.IntegerField(required=True)
