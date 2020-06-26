from django.contrib import admin
from .models import Calendar, Symptom, Appointment, Medicine, Advice, Disease

admin.site.register(Calendar)
admin.site.register(Symptom)
admin.site.register(Appointment)
admin.site.register(Medicine)
admin.site.register(Advice)
admin.site.register(Disease)
