from rest_framework import serializers
from .models import Calendar, Symptom, Disease, Advice, Medicine, Appointment
from account.models import Doctor, Patient
from account.serializer import DoctorSerializer, PatientSerializer
import datetime


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        doctor = Doctor.objects.get(user_id=self.context['request'].user.id)
        validated_data["doctor_id"] = doctor.id
        return super().create(validated_data)


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = "__all__"
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        doctor = Doctor.objects.get(user_id=self.context['request'].user.id)
        validated_data["doctor_id"] = doctor.id
        return super().create(validated_data)


class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = "__all__"
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        doctor = Doctor.objects.get(user_id=self.context['request'].user.id)
        validated_data["doctor_id"] = doctor.id
        return super().create(validated_data)


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"
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


class DoctorField(serializers.StringRelatedField):
    def to_representation(self, value):
        return value.first_name + " " + value.last_name


class PatientCalendarSerializer(serializers.ModelSerializer):
    doctor = DoctorField()
    speciality = serializers.ReadOnlyField(source="doctor.speciality")

    class Meta:
        model = Calendar
        fields = ["id", "day", "start_time", "remained",
                  "doctor", "speciality", "doctor_id"]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, data):
        turn = data["turn"]
        if turn.accepted == False:
            raise serializers.ValidationError(
                "This turn still not accepted")
        if turn.visited == True:
            raise serializers.ValidationError(
                "This turn already has an appointment")
        return data

    def create(self, validated_data):
        turn = validated_data["turn"]
        if turn.doctor.user.id != self.context['request'].user.id:
            raise serializers.ValidationError("You can't visit this turn")
        turn.visited = True
        turn.save()
        return super().create(validated_data)


class AppointmentSerializerRecursive(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    advices = AdviceSerializer(many=True)
    symptoms = SymptomSerializer(many=True)
    medicines = MedicineSerializer(many=True)
    disease = DiseaseSerializer(many=True)

    class Meta:
        model = Appointment
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = "__all__"


class TurnReserveSerializer(serializers.Serializer):
    action = serializers.MultipleChoiceField(
        choices=["accept", "reject"], required=True)
    calendar_id = serializers.IntegerField(required=True)
