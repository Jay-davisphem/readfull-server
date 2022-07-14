from rest_framework import permissions


class IsObjectOrAdminMixin(permissions.BasePermission):
    auth = False
    user = "user"

    def has_permission(self, request, view):
        if self.auth:
            return request.user.is_authenticated
        if view.action in ("list", "retrieve"):
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if self.user == "user":
            return obj.user == request.user or request.user.is_superuser
        elif self.user == "author":
            return obj.author == request.user or request.user.is_superuser
        elif self.user == "ch_author":
            return obj.novel.author == request.user or request.user.is_superuser
        elif self.user == "commentor":
            return obj.commentor == request.user or request.user.is_superuser
        elif self.user == "responder":
            return obj.responder == request.user or request.user.is_superuser
        return False


class IsOwnerOrAdmin(IsObjectOrAdminMixin):
    auth = True


class IsAuthorOrAdmin(IsObjectOrAdminMixin):
    user = "author"


class IsNovelistOrAdmin(IsObjectOrAdminMixin):
    user = "ch_author"


class IsCommenterOrAdmin(IsObjectOrAdminMixin):
    user = "commentor"


class IsResponderOrAdmin(IsObjectOrAdminMixin):
    user = "responder"
