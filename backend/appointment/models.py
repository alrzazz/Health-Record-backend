from django.db import models
from account.models import Doctor, Patient


class Turn(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="doctor_turn")
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="patient_turn", null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    accepted = models.BooleanField(default=False)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return "{}- {} to {}".format(self.id, self.start_time, self.end_time)


class Symptom(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    kind = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    value = models.FloatField()

    def __str__(self):
        return self.name


class Disease(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Advice(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class Medicine(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    duration = models.DurationField()

    def __str__(self):
        return self.name


class Appointment(models.Model):
    turn = models.OneToOneField(Turn, on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptom)
    disease = models.ManyToManyField(Disease)
    advices = models.ManyToManyField(Advice)
    medicines = models.ManyToManyField(Medicine)

    def __str__(self):
        return self.turn.__str__()
