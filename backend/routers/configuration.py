from typing import Annotated

from aiohttp import ClientSession
from fastapi import APIRouter, Depends
from yarl import URL

from backend.dependencies import get_http_client, get_plex_auth_token
from backend.external.plex_api import get_servers
from backend.external.plex_media_server import check_server_connection
from backend.models.plex import PlexServer

router = APIRouter(prefix='/api/v1')


@router.get('/get-plex-servers')
async def get_plex_servers(
    http: Annotated[ClientSession, Depends(get_http_client)],
    plex_auth_token: Annotated[str, Depends(get_plex_auth_token)],
) -> list[PlexServer]:
    plex_servers = await get_servers(http, plex_auth_token)
    return plex_servers


@router.get('/test-connection')
async def test_connection(
    http: Annotated[ClientSession, Depends(get_http_client)],
    url: str,
    token: str,
):
    success = await check_server_connection(
        client=http,
        url=URL(url),
        token=token,
    )
    return {'success': success}
