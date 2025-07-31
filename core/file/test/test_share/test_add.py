from file.models import UserFile
from rest_framework.test import APITestCase
from globals.test_objects import create_user, create_headers, create_user_file
from django.urls import reverse


class TestEndpoint(APITestCase) : 

    def setUp(self):
        self.endpoint = reverse('share-files')
    
    
    def test_unauthorized(self) :
        data = {
            "file" : 1,
            'users' : [1,2,3]
        }
        req = self.client.post(self.endpoint, data=data)
        self.assertEqual(req.status_code, 401)
    
    def test_forbidden(self) :
        user = create_user()
        file = create_user_file()
        data = {
            'users' : [
                create_user().id,
                create_user().id
            ],
            'file' : file.id
        }
        req = self.client.post(self.endpoint, data=data, headers=create_headers(user))
        self.assertEqual(req.status_code, 403)

    def test_invalid_file(self) :
        user = create_user()
        data = {
            'users' : [
                create_user().id,
                create_user().id
            ],
            'file' : 1000  
        }
        req = self.client.post(self.endpoint, data=data, headers=create_headers(user))
        self.assertEqual(req.status_code, 400)
    
    def test_invalid_users(self) :
        user = create_user()
        file = create_user_file(owner=user)
        data = {
            'users' : [1000, 2000], 
            'file' : file.id
        }
        req = self.client.post(self.endpoint, data=data, headers=create_headers(user))
        self.assertEqual(req.status_code, 400)

    def test_empty_body(self) : 
        admin_user = create_user(
            is_superuser=True,
        )
        req = self.client.post(self.endpoint, headers=create_headers(admin_user))
        self.assertEqual(req.status_code, 400)


    def test_success (self) : 
        user = create_user()
        file = create_user_file(owner=user, shared_with=[create_user()])
        data = {
            'users' : [
                create_user().id,
                create_user().id
            ],
            'file' : file.id
        }
        req = self.client.post(self.endpoint, data=data, headers=create_headers(user))
        self.assertEqual(req.status_code, 201)
        self.assertEqual(
            len(data['users']) + 1,
            UserFile.objects.get(id=file.id).shared_with.count()
        )