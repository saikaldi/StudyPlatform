from rest_framework.permissions import BasePermission

# class IsApprovedAdminManagerTeacher(BasePermission):
#     def has_permission(self, request, view):
#         if not request.user.is_authenticated:
#             return False
#         return bool(request.user.is_status_approved and request.user.user_status in ["Менеджер", "Админ", "Учитель"])

class IsAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS']
