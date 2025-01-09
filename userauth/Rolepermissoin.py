from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Student'

# class IsStudent(BasePermission):
#     def has_permission(self, request, view):
#         print(f"User: {request.user}")
#         print(f"Authenticated: {request.user.is_authenticated}")
#         print(f"Role: {getattr(request.user, 'role', None)}")
#         return (
#             request.user
#             and request.user.is_authenticated
#             and getattr(request.user, 'role', None) == 'Student'
#         )