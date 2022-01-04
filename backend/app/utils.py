from typing import Optional

from fastapi import Request, Response

from settings import FrontendSettings, conf

# Utilities that depend on the app


def set_cookie(
    response: Response,
    key: str,
    value: str,
    max_age: Optional[int] = None,
    path="/",
    http_only=True,
    samesite="Strict",
):
    """
    Store a cookie
    """
    secure = conf.COOKIE_SECURE
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        path=path,
        httponly=http_only,
        secure=secure,
        samesite=samesite,
    )


def get_frontend_settings_by_path(path_prefix: str) -> FrontendSettings:
    """
    Get the Frontend Settings for a frontend by it's path_prefix
    """
    frontend_settings_by_path = {f.path_prefix: f for f in conf.FRONTEND_APPS}
    return frontend_settings_by_path[path_prefix]


def url_for(req: Request, name: str, **kwargs) -> str:
    """
    Get the URL for a route, absolute with our own BASE_URL
    """
    relative_url = req.scope["router"].url_path_for(name, **kwargs)
    return f"{str(conf.BASE_URL).rstrip('/')}{relative_url}"
