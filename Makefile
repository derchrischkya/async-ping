start:
	docker-compose up -d
	python3.8 -m venv venv
	python3.8 -m pip install -r requirements.txt
	. venv/bin/activate
	nohup dotenv -f src/.env run -- python3.8  src/main.py > /dev/null 2>&1 &
	nohup dotenv -f microservices/.env run -- python3.8 microservices/ping.py > /dev/null 2>&1 &

stop:
	kill -9 $$(ps xu | grep "src/main.py" | grep -v grep | awk '{print $$2}')
	kill -9 $$(ps xu | grep "microservices/ping.py" | grep -v grep | awk '{print $$2}')
	docker-compose down