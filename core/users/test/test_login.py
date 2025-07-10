from globals.test_objects import create_user
from rest_framework.test import APITestCase
from django.urls import reverse

class TestLoginAPI (APITestCase) :

    def setUp(self):
        self.endpoint = reverse('login')

    def test_no_body(self) : 
        req = self.client.post(self.endpoint)
        self.assertEqual(req.status_code, 400)

    def test_invalid_email(self) : 
        data = {
            'email' : "123@gmail.com",
            'password' : '123',
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 401)

    def test_invalid_password(self) :
        user = create_user(password='12345') 
        data = {
            'email' : user.email,
            'password' : '123',
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 401)

    
    def test_success(self) :
        user = create_user(password='123') 
        data = {
            'email' : user.email,
            'password' : '123',
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 200)

