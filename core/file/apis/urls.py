from django.urls import path
from .views import (
    get,
    delete
)

urlpatterns = [
    path('get/v1/', get.ListUserFielAPI.as_view(), name='list-user-file'),
    path('get/v1/<int:id>/', get.RetrieveUserFielAPI.as_view(), name='retrieve-user-file'),
    path('delete/v1/<int:id>/', delete.DeleteUserFielAPI.as_view(), name='delete-user-file'),
]