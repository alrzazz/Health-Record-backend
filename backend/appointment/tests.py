from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User, Patient, Doctor
import datetime

manager = {
    "username": "0000000000",
    "password": "0000000000",
    "email": "0@gmail.com"
}

test_doctor1 = {
    "user": {
        "username": "1111111111",
        "password": "1111111111",
        "email": "1@gmail.com"
    },
    "first_name": "1111111111",
    "last_name": "1111111111",
    "mobile_number": "09111111111",
    "address": "1111111111",
    "birth_date": "1111-11-11",
    "gender": "0",
    "phone_number": "111-11111111",
    "speciality": "1111111111"
}

test_patient1 = {
    "user": {
        "username": "2222222222",
        "password": "2222222222",
        "email": "2@gmail.com"
    },
    "first_name": "2222222222",
    "last_name": "2222222222",
    "mobile_number": "09222222222",
    "address": "2222222222",
    "birth_date": "1111-11-11",
    "gender": "0",
}

advice1 = {
            "name": "advice1",
            "description": "description1"
            }

disease1 = {
            "name": "disease1"
            }

symptom1 = {
            "name": "symptom1",
            "value": "high"
            }

medicine1 = {
            "name": "medicine1",
            "duration": "4 00:00:00"
            }

class DoctorActionsTests(APITestCase):
    
    def setUp(self):
        User.objects.create_superuser(**manager)
        body = {"username": "0000000000",
                "password": "0000000000"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login manager
        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        self.client.post(reverse("account:manage:doctors-list"), test_doctor1, format='json') # create doctor
        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login doctor
        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access) 


    def test_create_advice(self):
        url = reverse("appointment:doctor:advices-list")
        response = self.client.post(url, advice1, format='json') # create a advice
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url, format='json') # list advices
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0], { "id": 1,
                                                        "name": "advice1",
                                                        "description": "description1"})

    def test_create_disease(self):
        url = reverse("appointment:doctor:diseases-list")
        response = self.client.post(url, disease1, format='json') # create a disease
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url, format='json') # list diseases
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0], { "id": 1,
                                                        "name": "disease1"})

    def test_create_symptom(self):
        url = reverse("appointment:doctor:symptoms-list")
        response = self.client.post(url, symptom1, format='json') # create a symptom
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url, format='json') # list symptoms
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0], { "id": 1,
                                                        "name": "symptom1",
                                                        "value": "high"})

    def test_create_medicine(self):
        url = reverse("appointment:doctor:medicines-list")
        response = self.client.post(url, medicine1, format='json') # create a medicine
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url, format='json') # list medicines
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0], { "id": 1,
                                                        "name": "medicine1",
                                                        "duration": "4 00:00:00"})

    def test_create_calendar(self):
        url = reverse("appointment:doctor:calendars-list")
        body = {"start_time":"14:00:00",
                "total":"20"}
        body["day"] = str(datetime.date.today() + datetime.timedelta(weeks=3,days=1)) # should time delta less than 3 weeks for correct day 
        response = self.client.post(url, body, format='json') # create a calendar with error for wrong day
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        day = str(datetime.date.today() + datetime.timedelta(days=5))
        body["day"] = day
        response = self.client.post(url, body, format='json') # create a calendar
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(url, format='json') # list calendars
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0], { "id": 1,
                                                        "day": day,
                                                        "start_time":"14:00:00",
                                                        "total":20,
                                                        "remained":20})
class PatientActionsTests(APITestCase):
    
    def setUp(self):
        User.objects.create_superuser(**manager)
        body = {"username": "0000000000",
                "password": "0000000000"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login manager

        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        self.client.post(reverse("account:manage:doctors-list"), test_doctor1, format='json') # create doctor
        self.client.post(reverse("account:manage:patients-list"), test_patient1, format='json') # create patient

        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login doctor

        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        calendar_body = {"start_time":"14:00:00",
                         "total":"20"}
        calendar_body["day"] = str(datetime.date.today() + datetime.timedelta(days=2))
        self.client.post(reverse("appointment:doctor:calendars-list"), body, format='json') # create a calendar
        body["day"] = str(datetime.date.today() + datetime.timedelta(days=3))
        calendar_body["total"] = 10
        self.client.post(reverse("appointment:doctor:calendars-list"), calendar_body, format='json') # create another calendar
        self.client.post(reverse("appointment:doctor:calendars-list"), calendar_body, format='json') # create another calendar


    def test_list_turns(self):
        url = reverse("account:login-user")
        body = {"username": "2222222222",
                "password": "2222222222"}
        response = self.client.post(url, body, format='json') # login patient
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.get(reverse("appointment:patient:turns-list")) # get all availibale turns
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
    
    def test_reserve_turn(self):
        url = reverse("account:login-user")
        body = {"username": "2222222222",
                "password": "2222222222"}
        response = self.client.post(url, body, format='json') # login patient
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.get(reverse("appointment:patient:turns-detail", kwargs={'pk': 1}), format='json') # get first turn details
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["doctor"]["id"], 1)
        self.assertEqual(response.data["remained"], 10)
        response = self.client.post(reverse("appointment:patient:turns-list"),  {"action":"accept", "calendar_id":1}, format='json') # reserve first turn
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Your Turn reserved'})

class AppointmentTests(APITestCase):
    
    def setUp(self):
        User.objects.create_superuser(**manager)
        body = {"username": "0000000000",
                "password": "0000000000"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login manager

        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        self.client.post(reverse("account:manage:doctors-list"), test_doctor1, format='json') # create doctor
        self.client.post(reverse("account:manage:patients-list"), test_patient1, format='json') # create patient

        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login doctor

        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        calendar_body = {"start_time":"14:00:00",
                         "total":"20"}
        calendar_body["day"] = str(datetime.date.today() + datetime.timedelta(days=2))
        self.client.post(reverse("appointment:doctor:calendars-list"), body, format='json') # create a calendar
        body["day"] = str(datetime.date.today() + datetime.timedelta(days=3))
        calendar_body["total"] = 10
        self.client.post(reverse("appointment:doctor:calendars-list"), calendar_body, format='json') # create another calendar
        self.client.post(reverse("appointment:doctor:calendars-list"), calendar_body, format='json') # create another calendar
        self.client.post(reverse("appointment:doctor:advices-list"), advice1, format='json') # create a advice
        self.client.post(reverse("appointment:doctor:diseases-list"), disease1, format='json') # create a disease
        self.client.post(reverse("appointment:doctor:symptoms-list"), symptom1, format='json') # create a symptom
        self.client.post(reverse("appointment:doctor:medicines-list"), medicine1, format='json') # create a medicine

        body = {"username": "2222222222",
                "password": "2222222222"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login patient

        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        self.client.post(reverse("appointment:patient:turns-list"),  {"action":"accept", "calendar_id":1}, format='json')

    def test_doctor_list_appointment(self):
        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login doctor
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.get(reverse("appointment:doctor:appointments-list"), format='json') # list all appoitments for doctor
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["patient"]["first_name"], "2222222222")
    
    def test_doctor_add_item_appointment(self):
        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login doctor
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.patch(reverse("appointment:doctor:appointments-detail", kwargs={'pk': 1}), {"advices":[1], "medicines":[1]}, format='json') # add item to appoitment
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["advices"], [1])
        self.assertEqual(response.data["medicines"], [1])

    def test_patient_get_appointment(self):
        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login doctor
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.patch(reverse("appointment:doctor:appointments-detail", kwargs={'pk': 1}), {"advices":[1], "medicines":[1], "dieseases":[1]}, format='json') # add item to appoitment
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        body = {"username": "2222222222",
                "password": "2222222222"}
        response = self.client.post(reverse("account:login-user"), body, format='json') # login patient
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.get(reverse("appointment:patient:appointments-list"), format='json') # get appointments
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["calendar"]["doctor"]["id"], 1)
        self.assertEqual(response.data["results"][0]["advices"][0]["name"], "advice1")
