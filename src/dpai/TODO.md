### Functional
- Websocket version:
https://medium.com/@nmjoshi/getting-started-websocket-with-fastapi-b41d244a2799
WebSocket with Swagger
- When loading model, hugging face model can be too big to save as joblib, create a strategy for loading the model in this case
- Provide update utility
- Allow torch/pickle/sklearn types of model input
- `model_manager.py` - enforce Singleton pattern with right locking mechanisms (also need to change the test case)


### Non-Functional
- logging compatibility issue
REST API version:
- Setup Distributed Tracing (Grafana Tempo + OpenTelemetry) & Metric Performance Monitoring (Prometheus)
- setup cors: https://fastapi.tiangolo.com/tutorial/cors/


### Docs
[docs]
- add limitations
- add advanced features after implemented

[readme]
- add architecture diagram


### Others
- When Celery component: add `try/except KeyboardInterrupt` as a potential fix to continuing celery worker
- Kafka component: add APIs for submitting data to and listening result from kafka - refer to aporio docs