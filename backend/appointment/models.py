from django.db import models
from account.models import User


class Turn(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, required=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    accepted = models.BooleanField(default=False)
    visited = models.BooleanField(default=False)


class Symptom(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    value = models.FloatField(required=False)


class Disease(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Advice(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()


class Medicine(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    duration = models.DurationField()


class Appointment(models.Model):
    turn = models.OneToOneField(Turn)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    advice = models.ForeignKey(Advice, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
