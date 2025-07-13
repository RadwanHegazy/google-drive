from rest_framework.test import APITestCase
from django.urls import reverse
from globals.test_objects import create_user, create_headers, create_storage_plan

class TestSubscribeEndpoint(APITestCase) : 

    def endpoint (self, id) :
        return reverse('plan-subscribe', args=[id])

    def test_unautenticated(self) :
        req = self.client.get(self.endpoint(10))
        self.assertEqual(req.status_code, 401)

    def test_not_found(self) : 
        req = self.client.get(self.endpoint(10), headers=create_headers())
        self.assertEqual(req.status_code, 404)

    
    def test_success(self) : 
        plan = create_storage_plan()
        req = self.client.get(self.endpoint(plan.id), headers=create_headers())
        self.assertEqual(req.status_code, 200)