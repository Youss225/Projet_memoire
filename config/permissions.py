from rest_framework.permissions import BasePermission


class EstOperateur(BasePermission):

    def has_permission(self, request, view):
        return True


"""class EstComptable(BasePermission):

    def has_permission(self, request, view):
        return True
"""

class EstComptable(BasePermission):

    def has_permission(self, request, view):

        print("USER :", request.user)
        print("AUTH :", request.user.is_authenticated)
        print(
            "GROUPES :",
            list(
                request.user.groups.values_list(
                    "name",
                    flat=True
                )
            )
        )

        return (
            request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.groups.filter(
                    name="Comptable"
                ).exists()
            )
        )