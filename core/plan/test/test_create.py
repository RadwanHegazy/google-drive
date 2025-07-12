from rest_framework.test import APITestCase
from globals.test_objects import create_storage_plan, create_user, create_headers
from django.urls import reverse


class TestEndpoint(APITestCase) : 

    def setUp(self):
        self.endpoint = reverse('create-storage-plan')
    
    
    def test_not_admin(self) :
        normal_user = create_user()
        data = {
            "name" : "My Plane",
            "storage_in_giga" : 10,
            "price_per_month" : 10.5,
            "price_per_year" : 3.5
        }
        req = self.client.post(self.endpoint, data=data, headers=create_headers(normal_user))
        self.assertEqual(req.status_code, 403)
        
    
    def test_unauthorized(self) :
        
        data = {
            "name" : "My Plane",
            "storage_in_giga" : 10,
            "price_per_month" : 10.5,
            "price_per_year" : 3.5
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 401)

    def test_empty_body(self) : 
        admin_user = create_user(
            is_superuser=True,
            is_staff=True
        )
        req = self.client.post(self.endpoint, headers=create_headers(admin_user))
        self.assertEqual(req.status_code, 400)

    def test_non_unique_name(self) : 
        p = create_storage_plan()
        admin_user = create_user(
            is_superuser=True,
            is_staff=True
        )
        data = {
            "name" : p.name,
            "storage_in_giga" : 10,
            "price_per_month" : 10.5,
            "price_per_year" : 3.5
        }
        req = self.client.post(self.endpoint, data=data, headers=create_headers(admin_user))
        self.assertEqual(req.status_code, 400)
    
    def test_success(self) : 
        admin_user = create_user(
            is_superuser=True,
            is_staff=True
        )
        data = {
            "name" : "My Plan",
            "storage_in_giga" : 10,
            "price_per_month" : 10.5,
            "price_per_year" : 3.5
        }
        req = self.client.post(self.endpoint, data=data, headers=create_headers(admin_user))
        self.assertEqual(req.status_code, 201)
        res = req.json()

        self.assertEqual(res['name'], data['name'])
        self.assertEqual(res['storage_in_giga'], data['storage_in_giga'])
        self.assertEqual(res['price_per_month'], data['price_per_month'])
        self.assertEqual(res['price_per_year'], data['price_per_year'])