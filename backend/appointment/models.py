from django.db import models
from account.models import Doctor, Patient
from django.core.validators import MinLengthValidator, MinValueValidator
import datetime


class Calendar(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="calendar_doctor")
    day = models.DateField()
    start_time = models.TimeField()
    total = models.IntegerField()
    remained = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Symptom(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': ("This symptom already exist."),
    })
    value = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Disease(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': ("This disease already exist."),
    })

    def __str__(self):
        return self.name


class Advice(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': ("This advice already exist."),
    })
    description = models.TextField()

    def __str__(self):
        return self.name


class Medicine(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': ("This medicine already exist."),
    })
    duration = models.DurationField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointment_patient")
    done = models.BooleanField(default=False)
    turn = models.IntegerField()
    symptoms = models.ManyToManyField(Symptom, blank=True)
    disease = models.ManyToManyField(Disease, blank=True)
    advices = models.ManyToManyField(Advice, blank=True)
    medicines = models.ManyToManyField(Medicine, blank=True)

    def __str__(self):
        return str(self.id)
