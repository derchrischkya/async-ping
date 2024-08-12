import uuid
import logging
import json
from fastapi import APIRouter, Depends, HTTPException
from modules.redis import Redis
from modules.nsq import NSQPublisher
from api.v1.exceptions import handle_exceptions
from api.v1.schemas import Response, MetaData
from elasticapm.traces import execution_context
from starlette.status import HTTP_202_ACCEPTED

router = APIRouter()
PATH = "/api/v1"

@router.get(f"{PATH}/async-ping", status_code=HTTP_202_ACCEPTED)
@handle_exceptions
async def ping_router() -> Response:
    log = logging.getLogger(__name__)
    id = str(uuid.uuid4())
    trace_parent = execution_context.get_transaction().trace_parent.to_string()

    log.info({"id": id, "message": "Ping request initiated", "trace_parent": trace_parent})

    meta = MetaData(trace_id=trace_parent, id=id, is_async=True, state="PENDING")
    response_payload = {"meta": json.loads(meta.json()), "event": {}}

    try:
        Redis().write(key=id, value=json.dumps(response_payload))
        log.info({"id": id, "message": "Payload stored in Redis"})
        
        NSQPublisher().publish(topic="ping", message=json.dumps(response_payload["meta"]).encode("utf-8"))
        log.info({"id": id, "message": "Payload published to NSQ"})
        
    except Exception as e:
        log.error({"id": id, "message": "Operation failed", "error": str(e)})
        raise HTTPException(status_code=500, detail="Internal Server Error")

    response_payload["redirect_uri"] = f"{PATH}/state/{id}"
    return Response(**response_payload)