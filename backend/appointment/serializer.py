from rest_framework import serializers
from .models import Turn, Symptom, Disease, Advice, Medicine, Appointment
from account.models import Doctor, Patient


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = "__all__"
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        symptom = Symptom.objects.create(
            **validated_data, doctor=Doctor.objects.get(user_id=self.context['request'].user.id))
        return symptom


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = "__all__"
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        disease = Disease.objects.create(
            **validated_data, doctor=Doctor.objects.get(user_id=self.context['request'].user.id))
        return disease


class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        fields = "__all__"
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        advice = Advice.objects.create(
            **validated_data, doctor=Doctor.objects.get(user_id=self.context['request'].user.id))
        return advice


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"
        extra_kwargs = {'doctor': {'read_only': True}}

    def create(self, validated_data):
        medicine = Medicine.objects.create(
            **validated_data, doctor=Doctor.objects.get(user_id=self.context['request'].user.id))
        return medicine


class TurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = "__all__"
        extra_kwargs = {'doctor': {'read_only': True},
                        'patient': {'read_only': True},
                        'accepted': {'read_only': True},
                        'visited': {'read_only': True}}

    def create(self, validated_data):
        return Turn.objects.create(**validated_data, doctor=Doctor.objects.get(user_id=self.context['request'].user.id))


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
        turn.visited = True
        turn.save()
        return super().create(validated_data)


class AppointmentSerializerRecursive(serializers.ModelSerializer):
    turn = TurnSerializer(read_only=True)
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


class TurnActionSerializer(serializers.Serializer):
    action = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(TurnActionSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        if data["action"] not in ["accept", "reject"]:
            raise serializers.ValidationError(
                "This acion is not valid")
        return data
