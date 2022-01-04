from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import List, Optional
from uuid import uuid4

import jwt
from fastapi import Cookie, HTTPException
from firedantic import ModelNotFoundError
from pydantic import BaseModel, Field
from pyjwt_key_fetcher import AsyncKeyFetcher
from pyjwt_key_fetcher.errors import JWTKeyFetcherError

from app.api import OpenIDConfiguration
from app.models import LoginState, LogoutState
from settings import conf


class User(BaseModel):
    id: str = Field(
        ..., title="User's pairwise ID", example="7f648110-505d-4960-868a-3dfdf0599cad"
    )


class Token(BaseModel):
    class Config:
        extra = "ignore"  # as per OpenID Connect specification

    iss: str = Field(..., title="Issuer Identifier")
    sub: str = Field(..., title="Subject identifier - User ID")
    aud: str = Field(..., title="Audience(s)")
    exp: int = Field(..., title="Expiration unix timestamp")
    iat: int = Field(..., title="Issued at unix timestamp")
    auth_time: Optional[int] = Field(None, title="Time of authentication")
    nonce: str = Field(..., title="Unique authentication nonce")
    acr: Optional[str] = Field(None, title="Authentication Context Class")
    amr: Optional[List[str]] = Field(None, title="Authentication Methods")
    azp: Optional[str] = Field(None, title="Authorized party")


async def get_openid_conf() -> OpenIDConfiguration:
    """
    Get the OpenID Connect configuration for our configured issuer.
    """
    fetcher = get_key_fetcher()
    conf_data = await fetcher.get_openid_configuration(conf.OPENID_CONNECT_ISSUER)
    return OpenIDConfiguration(**conf_data)


@lru_cache(maxsize=1)
def get_key_fetcher() -> AsyncKeyFetcher:
    """
    Create and return a singleton instance of the AsyncKeyFetcher
    """
    return AsyncKeyFetcher(valid_issuers=[conf.OPENID_CONNECT_ISSUER])


def generate_nonce() -> str:
    return str(uuid4())


async def parse_token(id_token: Optional[str]) -> User:
    if not id_token:
        raise HTTPException(401, "User not logged in")

    try:
        token = await validate_token(id_token=id_token)
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(401, "User not logged in")

    return User(id=token.sub)


async def validate_token(id_token: str) -> Token:
    """
    Validate an id_token
    raise: jwt.exceptions.InvalidTokenError If token is invalid
    """
    try:
        key_entry = await get_key_fetcher().get_key(id_token)
    except JWTKeyFetcherError as e:
        raise jwt.exceptions.InvalidTokenError from e
    token = Token(
        **jwt.decode(
            id_token,
            verify=True,
            audience=conf.OPENID_CONNECT_CLIENT_ID,
            issuer=conf.OPENID_CONNECT_ISSUER,
            **key_entry,
        )
    )

    return token


async def generate_state(return_path: str, nonce: str) -> str:
    """
    Generate a new state and store it in the database.
    """
    state = str(uuid4())
    ls = LoginState(
        id=state,
        expire=datetime.now(timezone.utc) + timedelta(hours=24),
        returnPath=return_path,
        nonce=nonce,
    )
    await ls.save()
    return state


async def generate_logout_state(
    redirect_target: str, state: Optional[str] = None
) -> str:
    """
    Generate a new logout state and store it in the database.
    """
    state_id = str(uuid4())
    ls = LogoutState(
        id=state_id,
        expire=datetime.now(timezone.utc) + timedelta(hours=24),
        redirect_target=redirect_target,
        state=state,
    )
    await ls.save()
    return state_id


async def get_valid_state(state: str) -> Optional[LoginState]:
    """
    Try to find a state in the database and verify it's still valid; return either None
    or the valid LoginState
    """
    try:
        ls = await LoginState.get_by_id(state)
    except ModelNotFoundError:
        return None

    await ls.delete()

    if ls.expire < datetime.now(timezone.utc):
        return None

    return ls


async def get_logged_in_user(id_token: str = Cookie(None)) -> User:
    """
    Get the currently logged in user; can be used as a dependency to require a user to
    be authenticated.
    """
    if not id_token:
        raise HTTPException(401, "Authentication required")

    return await parse_token(id_token)
