from rest_framework.test import APITestCase
from globals.test_objects import create_user_file, create_user, create_headers
from django.urls import reverse


class TestEndpoint(APITestCase) : 

    def endpoint(self, id):
        return reverse('retrieve-user-file', args=[id])

    
    def test_unauthenticated(self) : 
        req = self.client.get(self.endpoint(create_user_file().id))
        self.assertEqual(req.status_code, 401)
    
    def test_not_found(self) : 
        req = self.client.get(self.endpoint(10), headers=create_headers())
        self.assertEqual(req.status_code, 404)

    def test_unauthorized(self) : 
        model = create_user_file()
        req = self.client.get(self.endpoint(model.id), headers=create_headers())
        self.assertEqual(req.status_code, 403)
    

    def test_success(self) : 
        p = create_user_file()
        req = self.client.get(self.endpoint(p.id), headers=create_headers(p.owner))
        self.assertEqual(req.status_code, 200)
        res = req.json()
        self.assertEqual(res['name'], p.name)
        self.assertEqual(res['id'], p.id)

    def test_user_in_shared_with (self) : 
        friend = create_user()
        p = create_user_file(shared_with=[friend])
        req = self.client.get(self.endpoint(p.id), headers=create_headers(friend))
        self.assertEqual(req.status_code, 200)