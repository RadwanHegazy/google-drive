from globals.test_objects import create_user, create_headers
from rest_framework.test import APITestCase
from django.urls import reverse

class TestProfileAPI (APITestCase) :

    def setUp(self):
        self.endpoint = reverse('profile')

    def test_unauthorized(self) : 
        req = self.client.get(self.endpoint)
        self.assertEqual(req.status_code, 401)

    def test_success(self) :
        user = create_user()
        req = self.client.get(self.endpoint, headers=create_headers(user))
        self.assertEqual(req.status_code, 200)
        res = req.json()
        
        self.assertEqual(res['email'], user.email)
        self.assertEqual(res['full_name'], user.full_name)
        self.assertEqual(res['id'], user.id)
