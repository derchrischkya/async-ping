import uvicorn
import os
from api.http import app
import logging

logging.basicConfig(level=logging.INFO,
                    format="{\"time\": \"%(asctime)-s\", \"name\": \"%(name)s\", \"level\": \"%(levelname)-s\", \"message\": \"%(message)s\"}")
logger = logging.getLogger("webserver")
logger.info('Starting uvicorn.')

uvicorn.run(app, host=os.getenv("WEBAPP_HOST"), port=int(os.getenv('WEBAPP_PORT')), proxy_headers=True)