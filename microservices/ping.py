import json
import time
import os
import logging
import elasticapm
from modules.nsq_receiver import NSQReceiver
from modules.redis import Redis

# Initialize Elastic APM
os.environ["ELASTIC_APM_SERVICE_NAME"] = "microservices_ping"
elasticapm.instrument()
apm_client = elasticapm.Client()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize NSQ Receiver
receiver = NSQReceiver("ping", "ping_channel")

def process_message(message):
    try:
        data = json.loads(message.decode("utf-8"))
        logger.info("Received message: %s", data)
        
        # Start APM transaction
        trace_parent = elasticapm.trace_parent_from_string(data["trace_id"])
        apm_client.begin_transaction("script", trace_parent=trace_parent)
        elasticapm.set_transaction_name("ping")

        # Simulate processing
        time.sleep(5)  # Replace with actual logic

        # Prepare and save response
        data.update({"state": "COMPLETED", "updated_at": time.strftime("%Y-%m-%d %H:%M:%S%z")})
        response_payload = {"meta": data, "event": {"message": "ASYNC PONG"}}
        
        redis = Redis()
        redis.write(key=data["id"], value=json.dumps(response_payload))
        logger.info("Data written to Redis: %s", response_payload)

        # End APM transaction
        apm_client.end_transaction(name=__name__, result="success")

    except Exception as e:
        logger.error("Processing error: %s", e)
        apm_client.capture_exception()
        apm_client.end_transaction(name=__name__, result="failure")
        raise

# Assign processing function and start receiver
receiver.process_message = process_message
logger.info("NSQ Receiver started.")
receiver.start()