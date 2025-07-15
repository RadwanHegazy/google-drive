from rest_framework import serializers
from django.db import transaction
from plan.models import StoragePlan, UserTransaction, UserStoragePlan
import os
from plan.utlities import create_stripe_checkout_link

class StoragePlanSerializer (serializers.ModelSerializer) : 

    class Meta:
        model = StoragePlan
        fields = "__all__"


class CheckoutSerializer (serializers.Serializer) : 
    plan = serializers.PrimaryKeyRelatedField(
        queryset=StoragePlan.objects.all()
    )

    pay_every = serializers.ChoiceField(
        choices=['MONTH','YEAR']
    )

    amount = serializers.IntegerField(
        min_value=1
    )

     
    def create(self, validated_data):
        plan:StoragePlan = validated_data.get('plan')
        pay_every = validated_data.get('pay_every')
        amount = validated_data.get('amount')
        total_pay = amount * plan.price_per_month if pay_every == 'month' else amount * plan.price_per_year
        request = self.context.get('request')
        user = request.user

        line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': plan.name,
                },
                'unit_amount': int(total_pay * 100),  # (in cents)
            },
            'quantity': 1,
        }]
        
        with transaction.atomic() :
            try :
                session = UserTransaction.objects.create(
                    pay_every = pay_every,
                    subscribe_amount = amount,
                    plan = plan,
                    user = user
                )
                sucess_url = os.environ.get('STRIPE_SUCCESS_URL') + f"?session_id={session.id}"
                cancel_url = os.environ.get('STRIPE_CANCEL_URL') + f"?session_id={session.id}" 

                checkout_url = create_stripe_checkout_link(
                    line_items=line_items,
                    success_url=sucess_url,
                    cancel_url=cancel_url
                )

                self.checkout_url = checkout_url
            except Exception as error: 
                raise serializers.ValidationError({
                    'message' : "Transcation creation failed, please try again later",
                    'error' : str(error)
                })
            
            return True
        
    def to_representation(self, instance):
        return {
            'url' : self.checkout_url
        }

class SuccessChecoutSerializer (serializers.Serializer) : 
    session = serializers.PrimaryKeyRelatedField(
        queryset=UserTransaction.objects.filter(
            status = UserTransaction.StatusChoices.PENDING
        )
    )

    def validate(self, attrs): 
        session:UserTransaction = attrs.get('session')
        request = self.context.get('request')
        user = request.user

        if session.user != user : 
            raise serializers.ValidationError({
                'message' : 'invalid session'
            })

        self.user = user
        return attrs
    
    def create(self, validated_data): 
        # create UserStoragePlan
        session:UserTransaction = validated_data.get('session')
        plan = session.plan
        user = session.user

        user_plan = UserStoragePlan.objects.create(
            plan = plan,
            pay_every = session.pay_every,
        )
        
        user.storage_plan = user_plan
        user.save()

        session.status = UserTransaction.StatusChoices.ACCEPTED
        session.save()
        
        return True

    def to_representation(self, instance):
        return {
            'message' : "operation successeded"
        }

class CancelChecoutSerializer (serializers.Serializer) : 
    session = serializers.PrimaryKeyRelatedField(
        queryset=UserTransaction.objects.filter(
            status = UserTransaction.StatusChoices.PENDING
        )
    )

    def validate(self, attrs): 
        session:UserTransaction = attrs.get('session')
        request = self.context.get('request')
        user = request.user

        if session.user != user : 
            raise serializers.ValidationError({
                'message' : 'invalid session'
            })

        self.user = user
        return attrs
    
    def create(self, validated_data): 
        # create UserStoragePlan
        session:UserTransaction = validated_data.get('session')
        session.status = session.StatusChoices.CANCELED
        session.save()

        return True

    def to_representation(self, instance):
        return {
            'message' : "Operation Cancelled"
        }

    