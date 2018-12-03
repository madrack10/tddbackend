from rest_framework import permissions


class SafeMethodsOnlyPermission(permissions.BasePermission):
    #Acces aux methosdes non destructive GET et HEAD
    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        return request.method in permissions.SAFE_METHODS


class OfferAuthorCanEditPermission(SafeMethodsOnlyPermission):
   # Autoriser tout le monde à répertorier ou afficher, 
   # mais seul l'auteur peut modifier les instances existantes
   def has_object_permission(self, request, view, obj=None):
        if obj is None:
            # Either a list or a create, so no author
            can_edit = True
        else:
            can_edit = request.user == obj.author
        return can_edit or super(OfferAuthorCanEditPermission, self).has_object_permission(request, view, obj)
