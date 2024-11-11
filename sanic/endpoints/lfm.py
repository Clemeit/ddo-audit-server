"""
LFM endpoints.
"""

import time

from constants.server import SERVER_NAMES_LOWERCASE
from models.api import LfmRequestApiModel, ServerLfmDataApiModel
from models.redis import ServerLFMs
from services.redis import get_lfms_by_server_name, set_lfms_by_server_name
from utils.server import is_server_name_valid

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

lfm_blueprint = Blueprint("lfm", url_prefix="/lfm", version=1)


# ===== Client-facing endpoints =====
@lfm_blueprint.get("")
async def get_all_lfms(request):
    """
    Method: GET

    Route: /lfm

    Description: Get all LFM posts from all servers from the Redis cache.
    """
    try:
        response = {}
        for server_name in SERVER_NAMES_LOWERCASE:
            response[server_name] = get_lfms_by_server_name(server_name).model_dump()
    except Exception as e:
        return json({"message": str(e)}, status=500)

    return json({"data": response})


@lfm_blueprint.get("/<server_name:str>")
async def get_lfms_by_server(request, server_name):
    """
    Method: GET

    Route: /lfm/<server_name:str>

    Description: Get all LFM posts from a specific server from the Redis cache.
    """
    if not is_server_name_valid(server_name):
        return json({"message": "Invalid server name"}, status=400)

    server_lfms = get_lfms_by_server_name(server_name)

    return json({"data": server_lfms.model_dump()})


# ===================================


# ======= Internal endpoints ========
@lfm_blueprint.post("")
async def set_lfms(request: Request):
    """
    Method: POST

    Route: /lfm

    Description: Set LFM posts in the Redis cache. Should only be called by DDO Audit Collections. Keyframes.
    """
    # validate request body
    try:
        body = LfmRequestApiModel(**request.json)
    except Exception:
        return json({"message": "Invalid request body"}, status=400)

    # update in redis cache
    try:
        for server_name, server_lfms in body.model_dump().items():
            server_data = ServerLfmDataApiModel(**server_lfms)
            server_lfms = ServerLFMs(
                lfms={lfm.id: lfm for lfm in server_data.data},
                lfm_count=len(server_data.data),
                last_updated=time.time(),
            )
            set_lfms_by_server_name(server_name, server_lfms)
    except Exception as e:
        return json({"message": str(e)}, status=500)

    return json({"message": "success"})


@lfm_blueprint.patch("")
async def update_lfms(request):
    """
    Method: PATCH

    Route: /lfm

    Description: Update LFM posts in the Redis cache. Should only be called by DDO Audit Collections. Delta updates.
    """
    # update in redis cache
    return json({"message": "success"})


# ===================================
