from uuid import uuid4
from rest_framework.test import APITestCase
from django.urls import reverse
from globals.test_objects import create_user, create_headers, create_storage_plan, create_user_transaction
from plan.models import UserTransaction

class TestSuccessTransactionEndpoint(APITestCase) : 

    def setUp(self):
        self.endpoint = reverse('success-plan-subscribe')

    def test_unautenticated(self) :
        req = self.client.post(self.endpoint)
        self.assertEqual(req.status_code, 401)

    def test_no_body(self) : 
        req = self.client.post(self.endpoint, headers=create_headers())
        self.assertEqual(req.status_code, 400)
    
    
    def test_not_found_session(self) : 
        user = create_user()
        data = {
            'session' : str(uuid4())
        }
        req = self.client.post(self.endpoint, headers=create_headers(user), data=data)
        self.assertEqual(req.status_code, 400)

    def test_not_session_owner(self) : 
        user = create_user()
        transaction = create_user_transaction()
        data = {
            'session' : str(transaction.id)
        }
        req = self.client.post(self.endpoint, headers=create_headers(user), data=data)
        self.assertEqual(req.status_code, 400)

    def test_not_pending_session(self) : 
        user = create_user()
        transaction = create_user_transaction(user=user, status=UserTransaction.StatusChoices.ACCEPTED)
        data = {
            'session' : str(transaction.id)
        }
        req = self.client.post(self.endpoint, headers=create_headers(user), data=data)
        self.assertEqual(req.status_code, 400)
    
    def test_success(self) : 
        user = create_user()
        transaction = create_user_transaction(user=user)
        data = {
            'session' : str(transaction.id)
        }
        req = self.client.post(self.endpoint, headers=create_headers(user), data=data)
        self.assertEqual(req.status_code, 201)

        self.assertTrue(
            UserTransaction.objects.filter(user=user, status=UserTransaction.StatusChoices.ACCEPTED).exists()
        )
