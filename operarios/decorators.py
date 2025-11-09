from functools import wraps
from django.http import HttpResponse


def allowed_users(allowed_roles=None):
    """Decorador que permite el acceso solo a usuarios que pertenezcan a alguno de los
    roles (grupos) listados en `allowed_roles`.

    Uso:
        @allowed_users(allowed_roles=['jefe_bodega'])
        def vista(...):
            ...

    Si el usuario no pertenece a ninguno de los grupos permitidos, devuelve
    un HttpResponse con estado 403 (Forbidden).
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Si no hay usuario autenticado o no pertenece a grupos, denegar
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                return HttpResponse('No autorizado', status=403)

            user_groups = [g.name for g in request.user.groups.all()]
            # Comprobar si existe intersección entre los grupos del usuario y los permitidos
            for role in allowed_roles:
                if role in user_groups:
                    return view_func(request, *args, **kwargs)

            return HttpResponse('No autorizado', status=403)

        return _wrapped_view

    return decorator
