from uuid import UUID

import httpx
from fastapi import APIRouter, Cookie, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
from firedantic import ModelNotFoundError
from httpx import HTTPError
from loguru import logger

from app.api import ConsentRequestResponse, RequestConsentRequest
from app.auth import User, get_logged_in_user
from app.models import Consent
from settings import conf

router = APIRouter()
timeout = httpx.Timeout(30)
client = httpx.AsyncClient(timeout=timeout)


@router.get(
    "/from/{from}/to/{to}",
    summary="Check consent",
    response_model=ConsentRequestResponse,
    tags=["consents"],
)
async def get_consent(
    from_: UUID = Path(..., alias="from"),
    to: UUID = Path(...),
    user: User = Depends(get_logged_in_user),
) -> Consent:
    """
    Check if a consent is granted or not.
    """
    consent_id = get_consent_id(from_, to)
    try:
        return await Consent.get_by_id(consent_id)
    except ModelNotFoundError:
        return Consent(id=consent_id)


@router.post(
    "/from/{from}/to/{to}",
    summary="Update consent",
    response_model=ConsentRequestResponse,
    tags=["consents"],
)
async def update_consent(
    params: ConsentRequestResponse,
    from_: UUID = Path(..., alias="from"),
    to: UUID = Path(...),
    user: User = Depends(get_logged_in_user),
):
    """
    Create or update a consent.
    """
    consent_id = get_consent_id(from_, to)
    consent = Consent(id=consent_id, **params.dict())
    await consent.save()

    return consent


def get_consent_id(from_: UUID, to: UUID) -> str:
    """
    Turn the from ID and to id into a string that can be used as a key in Firebase.
    """
    return f"{from_}_{to}"


@router.post(
    "/request",
    name="Request a consent",
    description="Request a consent for accessing data using Consent Provider",
    tags=["consents"],
)
async def request_consent(data: RequestConsentRequest, id_token: str = Cookie(...)):
    """
    Request a consent for accessing data using Consent Provider
    """
    url = f"{conf.CONSENT_PROVIDER_URL}/Consent/Request"
    headers = {"Authorization": f"Bearer {id_token}"}
    logger.debug("Requesting a consent", data)
    try:
        resp = await client.post(url, json=data.dict(by_alias=True), headers=headers)
    except HTTPError:
        logger.exception("Failed to communicate with Consent Provider")
        raise HTTPException(status_code=502)
    return JSONResponse(resp.json(), status_code=resp.status_code)
