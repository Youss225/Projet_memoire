from django.shortcuts import redirect


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        urls_autorisees = [
            "/login/",
            "/admin/login/",
            "/logout/",
        ]

        if (
            not request.user.is_authenticated
            and request.path not in urls_autorisees
            and not request.path.startswith("/media/")
            and not request.path.startswith("/admin/")
        ):
            return redirect("/login/")

        return self.get_response(request)