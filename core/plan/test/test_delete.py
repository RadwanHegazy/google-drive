from rest_framework.test import APITestCase
from globals.test_objects import create_storage_plan, create_user, create_headers
from django.urls import reverse
from django.core.cache import cache

class TestEndpoint(APITestCase) : 

    def endpoint(self, id):
        return reverse('delete-storage-plan', args=[id])

    
    def test_unauthenticated(self) : 
        p = create_storage_plan()
        req = self.client.delete(self.endpoint(p.id))
        self.assertEqual(req.status_code, 401)
    
    def test_unauthorized(self) : 
        user = create_user()
        p = create_storage_plan()
        req = self.client.delete(self.endpoint(p.id), headers=create_headers(user))
        self.assertEqual(req.status_code, 403)

    def test_not_found(self) : 
        user = create_user(
            is_staff=True,
            is_superuser=True
        )
        req = self.client.delete(self.endpoint(11), headers=create_headers(user))
        self.assertEqual(req.status_code, 404)

    def test_success(self) : 
        user = create_user(
            is_staff=True,
            is_superuser=True
        )
        p = create_storage_plan()
        plans = cache.get('plan')
        self.assertNotEqual(plans, [])

        req = self.client.delete(self.endpoint(p.id), headers=create_headers(user))
        self.assertEqual(req.status_code, 204)
        plans = cache.get('plan')
        self.assertEqual(plans, None)


    
    
