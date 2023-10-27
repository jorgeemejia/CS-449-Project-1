user_service: uvicorn --port $PORT user_service:app --reload
api: uvicorn --port $PORT api:app --reload
krakend: echo ./etc/krakend.json | entr -nrz krakend run --config etc/krakend.json --port $PORT