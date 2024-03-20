[Some Info]

- currently supported request type: `request_content_type=application/json`

[Instructions]

1. save your model in `.joblib` format. Example:

```python
from joblib import dump

your_model_artifact = {
    "model": your_model,
    # other metadata
    "tokenizer": ...,
    "quantization": ...,
    ...
}

dump(your_model_artifact, "MODEL_ARTIFACT_PATH.joblib")
```

2. Create inference script `inference.py` with two functions `input_fn` and `predict_fn` (similar to how [sagemaker inference](https://docs.aws.amazon.com/sagemaker/latest/dg/neo-deployment-hosting-services-prerequisites.html) does). Usually you'll create an inference file for each model you register. Example:

```python
def input_fn(data):
    processed_data_for_model_input = ...  # some transformation logic
    return processed_data_for_model_input

def predict_fn(input, model):
    result = model(input)
    return result
```

3. Register model: run `deployaible register --name=MODLE_NAME --model_path=MODEL_ARTIFACT_PATH_JOBLIB --inference_path=INFERENCE_SCRIPT_PATH`
4. Serve your model: run `deployaible serve --port=YOUR_PORT`
   You will get a backend running on `YOUR_PORT` (default is 9000). A sample endpoint will be `localhost:9000/your_model_name/predict`.
5. Test endpoint: run

```shell
curl -X POST -H "Content-Type: application/json" -d '{"data": ["val"]}' http://localhost:YOUR_PORT/GPT4/predict
```

6. You can also the APIs via swagger UI on `http://localhost:YOUR_PORT/docs`

sample_notebook_placeholder

sample_architecture_placeholder
