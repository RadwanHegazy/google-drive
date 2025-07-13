from django.db import models

class StoragePlan (models.Model) : 
    name = models.CharField(max_length=225, unique=True)
    storage_in_giga = models.FloatField()
    price_per_month = models.FloatField()
    price_per_year = models.FloatField()

    def __str__(self):
        return self.name
    
class UserStoragePlan (models.Model) : 
    plan = models.ForeignKey(
        StoragePlan,
        on_delete=models.CASCADE,
        related_name='user_storage_plan'
    )
    
    class PayEvery(models.TextChoices) : 
        YEAR = 'YEAR', 'YEAR'
        MONTH = 'MONTH', 'MONTH'
    
    pay_every = models.CharField(
        choices=PayEvery,
        max_length=10
    )

    subscribe_at = models.DateField(auto_now_add=True)

    @property
    def price (self) : 
        if self.pay_every == self.PayEvery.MONTH:
            return self.plan.price_per_month
        elif self.pay_every == self.PayEvery.YEAR:
            return self.plan.price_per_year * 12
        else:
            raise ValueError(f"There is no price for current plan : {self.plan.name}")


class UserTransaction (models.Model) : 
    user = models.ForeignKey(
        'users.User',
        related_name='user_transcation',
        on_delete=models.SET_NULL,
        null=True
    )

    plan = models.ForeignKey(
        StoragePlan,
        related_name='user_transaction_plan',
        on_delete=models.SET_NULL,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class StatusChoices (models.TextChoices) : 
        PENDING = "PENDING", "PENDING"
        ACCEPTED = "ACCEPTED", "ACCEPTED"
        CANCELED = "CANCELED", "CANCELED"
    
    status = models.CharField(
        choices=StatusChoices,
        max_length=20,
        default=StatusChoices.PENDING
    )