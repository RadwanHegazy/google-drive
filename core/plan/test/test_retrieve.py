from rest_framework.test import APITestCase
from globals.test_objects import create_storage_plan
from django.urls import reverse


class TestEndpoint(APITestCase) : 

    def endpoint(self, id):
        return reverse('retrieve-storage-plan', args=[id])

    def test_not_found(self) : 
        req = self.client.get(self.endpoint(10))
        self.assertEqual(req.status_code, 404)
    
    def test_success(self) : 
        p = create_storage_plan()
        req = self.client.get(self.endpoint(p.id))
        self.assertEqual(req.status_code, 200)
        res = req.json()
        self.assertEqual(res['name'], p.name)
        self.assertEqual(res['id'], p.id)