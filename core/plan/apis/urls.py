from django.urls import path
from .views import (
    get,
    update,
    delete,
    create,
    plan_checkout
)

urlpatterns = [
    path('get/v1/', get.ListStoragePlanAPI.as_view(), name='list-storage-plan'),
    path('get/v1/<int:id>/', get.RetrieveStoragePlanAPI.as_view(), name='retrieve-storage-plan'),
    path('update/v1/<int:id>/', update.UpdateStoragePlanAPI.as_view(), name='update-storage-plan'),
    path('delete/v1/<int:id>/', delete.DeleteStoragePlanAPI.as_view(), name='delete-storage-plan'),
    path('create/v1/', create.CreateStoragePlanAPI.as_view(), name='create-storage-plan'),
    path('subscribe/v1/',plan_checkout.UserPlanSubscribeAPI.as_view(), name='plan-subscribe'),
    path('subscribe/success/v1/',plan_checkout.SuccessSubscribeAPI.as_view(), name='success-plan-subscribe'),
    path('subscribe/cancel/v1/',plan_checkout.CancelSubscribeAPI.as_view(), name='cancel-plan-subscribe'),

]