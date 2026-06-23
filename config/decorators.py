from django.shortcuts import redirect

def groupe_requis(*groupes):

    def decorator(view_func):

        def wrapper(request, *args, **kwargs):

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if request.user.groups.filter(
                name__in=groupes
            ).exists():

                return view_func(
                    request,
                    *args,
                    **kwargs
                )

            return redirect("/")

        return wrapper

    return decorator