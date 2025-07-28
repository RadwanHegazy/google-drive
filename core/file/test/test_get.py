from rest_framework.test import APITestCase
from globals.test_objects import create_user_file, create_user, create_headers
from django.urls import reverse


class TestEndpoint(APITestCase) : 

    def setUp(self):
        self.endpoint = reverse('list-user-file')

    def test_unauthenticated(self) : 
        req = self.client.get(self.endpoint)
        self.assertEqual(req.status_code, 401)
    
    def test_empty(self) : 
        req = self.client.get(self.endpoint, headers=create_headers())
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.json(), [])
    
    def test_not_empty(self) : 
        model = create_user_file()
        req = self.client.get(self.endpoint, headers=create_headers(model.owner))
        self.assertEqual(req.status_code, 200)
        self.assertNotEqual(req.json(), [])
