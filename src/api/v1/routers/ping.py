import uuid
import logging
import json
from fastapi import APIRouter
from api.v1.exceptions import handle_exceptions
from api.v1.schemas import Response, MetaData
from elasticapm.traces import execution_context

router = APIRouter()
PATH = "/api/v1"

@router.get(f"{PATH}/ping")
@handle_exceptions
async def ping_router() -> Response:
    log = logging.getLogger(__name__)
    id = str(uuid.uuid4())
    trace_parent = execution_context.get_transaction().trace_parent.to_string()

    log.info({"id": id, "endpoint": f"{PATH}/ping", "message": "Ping request started"})

    response_payload = {
        "meta": json.loads(MetaData(trace_id=trace_parent, id=id).json()),
        "event": {"message": "SYNC PONG"}
    }
    return Response(**response_payload)
