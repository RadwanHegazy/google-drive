from django.urls import path
from .views import (
    get,
    update,
    delete,
    create,
    subscribe
)

urlpatterns = [
    path('get/v1/', get.ListStoragePlanAPI.as_view(), name='list-storage-plan'),
    path('get/v1/<int:id>/', get.RetrieveStoragePlanAPI.as_view(), name='retrieve-storage-plan'),
    path('update/v1/<int:id>/', update.UpdateStoragePlanAPI.as_view(), name='update-storage-plan'),
    path('delete/v1/<int:id>/', delete.DeleteStoragePlanAPI.as_view(), name='delete-storage-plan'),
    path('create/v1/', create.CreateStoragePlanAPI.as_view(), name='create-storage-plan'),
    path('subscribe/v1/<int:plan_id>/',subscribe.UserPlanSubscribe.as_view(), name='plan-subscribe')
]