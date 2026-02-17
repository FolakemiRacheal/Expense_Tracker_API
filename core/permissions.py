from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user
        
        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user

class IsNotDefaultCategory(permissions.BasePermission):
    """
    Prevent deletion/modification of default categories
    """
    def has_object_permission(self, request, view, obj):
        # Allow read operations
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Prevent modification/deletion of default categories
        if hasattr(obj, 'is_default') and obj.is_default:
            return False
        
        return True

class CanModifyTransaction(permissions.BasePermission):
    """
    Custom permission for transaction modifications
    """
    def has_object_permission(self, request, view, obj):
        # Only owner can modify
        if obj.user != request.user:
            return False
        
        # Prevent modification of transactions linked to processed receipts
        if hasattr(obj, 'receipt') and obj.receipt and obj.receipt.status == 'processed':
            return request.method in permissions.SAFE_METHODS
        
        return True