from django.urls import path
from .views import (
    get,
    delete,
    share
)

urlpatterns = [
    path('get/v1/', get.ListUserFielAPI.as_view(), name='list-user-file'),
    path('share/add/v1/', share.ShareFilesAPI.as_view(), name='share-files'),
    path('share/remove/v1/<int:id>/', share.RemoveSharedUsersAPI.as_view(), name='remove-share'),
    path('get/v1/<int:id>/', get.RetrieveUserFielAPI.as_view(), name='retrieve-user-file'),
    path('delete/v1/<int:id>/', delete.DeleteUserFielAPI.as_view(), name='delete-user-file'),
]