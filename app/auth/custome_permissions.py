from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User, Group, Permission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
# @permission_classes(['IsAuthenticated'])
class IsManager(BasePermission):
    def has_permission(self, request, view):
        position = request.user.position
        is_true = (position == "manager")
        return bool(is_true and request.user.is_authenticated)

@api_view(['GET', 'POST'])

class IsDataEntry(BasePermission):
    def has_permission(self, request, view):
        position = request.user.position
        is_true = (position == "data entry")
        return bool(is_true and request.user.is_authenticated)

"""
One way to add the permissions from a group model to a user is to use the Group and Permission
 models from django.contrib.auth.models. You can create a group with a name and assign it some
 permissions using the permissions field, which is a many-to-many relation. Then you can add a
 user to the group using the groups field of the user model, which is also a many-to-many relation.
 For example, you can do something like this:

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create a content type for your model
content_type = ContentType.objects.get(app_label='myapp', model='MyModel')

# Create a permission for your model
permission = Permission.objects.create(codename='can_do_something', name='Can do something', content_type=content_type)

# Create a group and assign it the permission
group = Group.objects.create(name='MyGroup')
group.permissions.add(permission)

# Get a user and add it to the group
user = User.objects.get(username='myuser')
user.groups.add(group)
Copy
This way, the user will have the permission from the group model. You can check if the user has
a permission using the has_perm method of the user model. For example:

user.has_perm('myapp.can_do_something') # True
Copy
I hope this helps you understand how to add the permissions from a group model to a user. 😊

Received message. To add the permissions from a group model to a user, you need
"""