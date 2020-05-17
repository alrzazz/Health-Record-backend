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
        return "{} date={}  remained={}".format(self.doctor, self.remained)


class Symptom(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    kind = models.IntegerField(default=0)
    name = models.CharField(max_length=50, unique=True, error_messages={
        'unique': ("This symptom already exist."),
    })
    value = models.FloatField()

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
    start_time = models.DateTimeField()
    turn = models.IntegerField()
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointment_doctor")
    Patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointment_doctor")
    symptoms = models.ManyToManyField(Symptom, blank=True)
    disease = models.ManyToManyField(Disease, blank=True)
    advices = models.ManyToManyField(Advice, blank=True)
    medicines = models.ManyToManyField(Medicine, blank=True)

    def __str__(self):
        return self.turn.__str__()
