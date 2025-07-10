from globals.test_objects import create_user
from rest_framework.test import APITestCase
from django.urls import reverse

class TestRegisterAPI (APITestCase) :

    def setUp(self):
        self.endpoint = reverse('register')

    def test_no_body(self) : 
        req = self.client.post(self.endpoint)
        self.assertEqual(req.status_code, 400)

    def test_invalid_email(self) : 
        data = {
            'email' : "123",
            'password' : '123',
            "full_name" : "Test"
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 400)


    def test_email_already_exists(self) :
        user = create_user(email='test@gmail.com') 
        data = {
            'email' : user.email,
            'password' : '123',
            "full_name" : "Test"
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 400)
    
    def test_success(self) :
        data = {
            'email' : "test@gmail.com",
            'password' : '123',
            'full_name' : 'Test'
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 201)

