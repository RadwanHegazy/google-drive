from rest_framework.permissions import BasePermission

class CanViewFile (BasePermission) : 

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return request.user in obj.shared_with.all()