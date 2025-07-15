from rest_framework.test import APITestCase
from django.urls import reverse
from globals.test_objects import create_user, create_headers, create_storage_plan
from plan.models import UserTransaction

class TestSubscribeEndpoint(APITestCase) : 

    def setUp(self):
        self.endpoint = reverse('plan-subscribe')

    def test_unautenticated(self) :
        req = self.client.post(self.endpoint)
        self.assertEqual(req.status_code, 401)

    def test_no_body(self) : 
        req = self.client.post(self.endpoint, headers=create_headers())
        self.assertEqual(req.status_code, 400)
    
    
    def test_not_found_plan(self) : 
        user = create_user()
        data = {
            'plan' : 10,
            'pay_every' : 'MONTH',
            'amount' : 2, # subscribe for 2 months
        }
        req = self.client.post(self.endpoint, headers=create_headers(user), data=data)
        self.assertEqual(req.status_code, 400)

    def test_no_amount(self) : 
        user = create_user()
        data = {
            'plan' : create_storage_plan().id,
            'pay_every' : 'MONTH',
            'amount' : 0,
        }
        req = self.client.post(self.endpoint, headers=create_headers(user), data=data)
        self.assertEqual(req.status_code, 400)

    def test_success(self) : 
        plan = create_storage_plan()
        user = create_user()
        data = {
            'plan' : plan.id,
            'pay_every' : 'MONTH',
            'amount' : 2, # subscribe for 2 months
        }
        req = self.client.post(self.endpoint, headers=create_headers(user), data=data)
        self.assertEqual(req.status_code, 201)

        user_tran = UserTransaction.objects.filter(user=user).first()

        self.assertEqual(
            user_tran.total_price,
            plan.price_per_month * data['amount']   
        )