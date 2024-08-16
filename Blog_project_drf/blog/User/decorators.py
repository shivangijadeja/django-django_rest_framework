def require_authentication(view_func):
    def wrapper(request, *args, **kwargs):
        auth_status = False
        if 'username' and 'secretkey' in request.session:
            auth_status=True
        kwargs["auth_status"] = auth_status
        return view_func(request, *args, **kwargs)
    return wrapper