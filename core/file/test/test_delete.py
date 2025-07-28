from rest_framework.test import APITestCase
from globals.test_objects import create_user_file, create_user, create_headers
from django.urls import reverse
from django.core.cache import cache

class TestEndpoint(APITestCase) : 

    def endpoint(self, id):
        return reverse('delete-user-file', args=[id])

    
    def test_unauthenticated(self) : 
        p = create_user_file()
        req = self.client.delete(self.endpoint(p.id))
        self.assertEqual(req.status_code, 401)
    
    def test_not_found(self) : 
        user = create_user()
        req = self.client.delete(self.endpoint(11), headers=create_headers(user))
        self.assertEqual(req.status_code, 404)
    
    def test_not_user_owner(self) : 
        user = create_user()
        req = self.client.delete(self.endpoint(create_user_file().id), headers=create_headers(user))
        self.assertEqual(req.status_code, 404)

    def test_success(self) : 
        user = create_user()
        p = create_user_file(owner=user)
        req = self.client.delete(self.endpoint(p.id), headers=create_headers(user))
        self.assertEqual(req.status_code, 204)
