from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include

schema_view = get_schema_view(
   openapi.Info(
      title="Google Drive API",
      default_version='v1',
      description="Google Drive APIs description",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.apis.urls')),
    path('plan/', include('plan.apis.urls')),


    path('__docs__/v1/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
