from typing import Optional

import httpx
from fastapi import APIRouter, Cookie, Header, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from httpx import HTTPError

from app.log import logger
from settings import conf

router = APIRouter()
timeout = httpx.Timeout(30)
client = httpx.AsyncClient(timeout=timeout)


@router.post("/{data_product:path}", tags=["data_product"])
async def route_identities(
    data_product: str,
    request: Request,
    id_token: str = Cookie(...),
    x_consent_token: Optional[str] = Header(None),
) -> Response:
    url = f"{conf.PRODUCT_GATEWAY_URL}/{data_product}"
    if request.url.query:
        url += f"?{request.url.query}"
    json_payload = await request.json()
    headers = {
        "Authorization": f"Bearer {id_token}",
        "X-Consent-Token": x_consent_token or "",
    }
    logger.debug("Fetching Data Product", url=url)
    try:
        resp = await client.post(url, json=json_payload, headers=headers)
    except HTTPError:
        logger.exception("Failed to fetch Data Product from the Product Gateway")
        raise HTTPException(status_code=502)

    response = JSONResponse(resp.json(), status_code=resp.status_code)
    for value in resp.headers.get_list("x-powered-by"):
        response.headers.append("x-powered-by", value)

    return response
