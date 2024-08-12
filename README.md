# Async Ping-Pong

This is a simple webserver that responds to a `GET` request in synchronous and asynchronous ways.

## Endpoints

- http://127.0.0.1:19000/api/v1/ping
- http://127.0.0.1:19000/api/v1/async-ping
- http://127.0.0.1:19000/api/v1/state/{id}

## Tools
- NSQ (Message Queue) - Persistence `nsq_data` folder
- Redis (Cache) - Persistence `redis_data` folder
- FastAPI (Web Framework)
- Uvicorn (ASGI Server)

## How to run

```bash
make start

```

## How to stop

```bash
make stop
```

## How to test

```bash
curl http://127.0.0.1:19000/api/v1/async-ping
```

```bash
curl http://127.0.0.1:19000/api/v1/state/{id}
```

## Monitoring

For the monitoring of the APM (Application Performance Monitoring) I used Elastic APM. The HEC Endpoint is defined in the `.env` file.



