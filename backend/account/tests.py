from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import User, Patient, Doctor


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

class AdminActionsTests(APITestCase):
    def setUp(self):
        User.objects.create_superuser(**manager)

    def test_login_admin(self):
        url = reverse("account:login-user")
        body = {"username": "0000000000",
                "password": "0000000000"}
        response = self.client.post(url, body, format='json') # login admin
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_doctor(self):
        url = reverse("account:login-user")
        body = {"username": "0000000000",
                "password": "0000000000"}
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data["access"]
        refresh = response.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        url = reverse("account:manage:doctors-list")
        response = self.client.post(url, test_doctor1, format='json') # create a doctor
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_patient(self):
        url = reverse("account:login-user")
        body = {"username": "0000000000",
                "password": "0000000000"}
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data["access"]
        refresh = response.data["refresh"]

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        url = reverse("account:manage:patients-list") # create a patient
        response = self.client.post(url, test_patient1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthenticationTest(APITestCase):

    def setUp(self):
        User.objects.create_superuser(**manager)
        body = {"username": "0000000000",
                "password": "0000000000"}
        response = self.client.post(reverse("account:login-user"), body, format='json')
        access = response.data["access"]
        refresh = response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        self.client.post(reverse("account:manage:doctors-list"), test_doctor1, format='json')
        self.client.post(reverse("account:manage:patients-list"), test_patient1, format='json')

    def test_login_user(self):
        url = reverse("account:login-user")
        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(url, body, format='json') # login a user
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        url = reverse("account:login-user")
        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(url, body, format='json')
        access = response.data["access"]
        refresh = response.data["refresh"]

        url = reverse("account:retrieve-user")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.get(url, format='json') # get user info
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 2, 'username': '1111111111', 'email': '1@gmail.com', 'role': 1})
    
    def test_profile_user(self):
        url = reverse("account:login-user")
        body = {"username": "2222222222",
                "password": "2222222222"}
        response = self.client.post(url, body, format='json')
        access = response.data["access"]
        refresh = response.data["refresh"]

        url = reverse("account:profile-user")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        response = self.client.get(url, format='json') # get profile
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "2222222222")

        body = {
            "first_name":"Ali"
        }
        response = self.client.patch(url, body, format='json') # update profile
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, format='json') # get profile
        self.assertEqual(response.data["first_name"], "Ali")

    def test_logout_user(self):
        url = reverse("account:login-user")
        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(url, body, format='json')
        access = response.data["access"]
        refresh = response.data["refresh"]

        url = reverse("account:logout-user")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        body = {
            "refresh":refresh
        }
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Logged out successfully'})

    def test_change_password_user(self):
        url = reverse("account:login-user")
        body = {"username": "1111111111",
                "password": "1111111111"}
        response = self.client.post(url, body, format='json')
        access = response.data["access"]
        refresh = response.data["refresh"]

        url = reverse("account:change-password")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        body = {
            "old_password":"222",
            "new_password1":"22222222",
            "new_password2":"222"
        }
        response = self.client.put(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body["new_password2"] = "22222222"
        response = self.client.put(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        body["old_password"] = "1111111111"
        response = self.client.put(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Password updated successfully'})

        url = reverse("account:login-user")
        body = {"username": "1111111111",
                "password": "22222222"}
        response = self.client.post(url, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
