from rest_framework.test import APITestCase
from globals.test_objects import create_storage_plan
from django.urls import reverse


class TestEndpoint(APITestCase) : 

    def setUp(self):
        self.endpoint = reverse('list-storage-plan')

    def test_invalid_method (self) : 
        req = self.client.post(self.endpoint)
        self.assertEqual(req.status_code, 405)

    def test_empty(self) : 
        req = self.client.get(self.endpoint)
        self.assertEqual(req.status_code, 200)
        self.assertEqual(req.json(), [])
    
    def test_not_empty(self) : 
        create_storage_plan()
        req = self.client.get(self.endpoint)
        self.assertEqual(req.status_code, 200)
        self.assertNotEqual(req.json(), [])

    
