import uuid
import logging
import json
from modules.redis import Redis
from fastapi import APIRouter
from api.v1.exceptions import handle_exceptions
from api.v1.schemas import Body, Response


router = APIRouter()
@router.get("/api/v1/state/{state_id}")
@handle_exceptions
async def state_read_router(state_id) -> Response:
    log = logging.getLogger(__name__)
    id = str(uuid.uuid4())
    log.info({"id": id, "endpoint": f"/api/v1/state/{state_id}", "message": "Read state of a async-api-ping request"})
    cache = json.loads(Redis().read(key=state_id).decode('utf-8'))
    return Response(**cache)


