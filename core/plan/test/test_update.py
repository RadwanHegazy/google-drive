from rest_framework.test import APITestCase
from globals.test_objects import create_storage_plan, create_user, create_headers
from django.urls import reverse

class TestEndpoint(APITestCase) : 

    def endpoint(self, id):
        return reverse('update-storage-plan', args=[id])

    
    def test_unauthenticated(self) : 
        p = create_storage_plan()
        req = self.client.put(self.endpoint(p.id))
        self.assertEqual(req.status_code, 401)
    
    def test_unauthorized(self) : 
        user = create_user()
        p = create_storage_plan()
        req = self.client.put(self.endpoint(p.id), headers=create_headers(user))
        self.assertEqual(req.status_code, 403)

    def test_not_found(self) : 
        user = create_user(
            is_staff=True,
            is_superuser=True
        )
        req = self.client.put(self.endpoint(11), headers=create_headers(user))
        self.assertEqual(req.status_code, 404)

    def test_success(self) : 
        user = create_user(
            is_staff=True,
            is_superuser=True
        )
        p = create_storage_plan()
        data = {
            "name" : "My New Plan Name",
            "storage_in_giga" : 100,
            "price_per_month" : 3.5,
            "price_per_year" : 1.5
        }
        req = self.client.put(self.endpoint(p.id), headers=create_headers(user), data=data)
        self.assertEqual(req.status_code, 200)

        res = req.json()

        self.assertEqual(res['name'], data['name'])
        self.assertEqual(res['storage_in_giga'], data['storage_in_giga'])
        self.assertEqual(res['price_per_month'], data['price_per_month'])
        self.assertEqual(res['price_per_year'], data['price_per_year'])

    
    def test_unique_name(self) : 
        user = create_user(
            is_staff=True,
            is_superuser=True
        )
        p = create_storage_plan()
        data = {
            "name" : p.name,
            "storage_in_giga" : 10.0,
            "price_per_month" : 3.5,
            "price_per_year" : 1.5
        }
        req = self.client.put(self.endpoint(p.id), headers=create_headers(user), data=data)
        self.assertEqual(req.status_code, 200)

        res = req.json()
        self.assertEqual(res['storage_in_giga'], data['storage_in_giga'])
