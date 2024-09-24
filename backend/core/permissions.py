from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    '''perm for admins'''
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='admin').exists()
    

class IsModerator(BasePermission):
    '''perm for moderators'''
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='moderator').exists()
    

class CanSell(BasePermission):
    '''checker for selling-access'''
    def has_permission(self, request, view):
        return request.user and request.user.selling_access