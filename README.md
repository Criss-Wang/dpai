![build](https://github.com/criss-wang/dpai/workflows/build/badge.svg) 
![docs](https://github.com/criss-wang/dpai/workflows/docs/badge.svg) 
![lint](https://github.com/criss-wang/dpai/workflows/lint/badge.svg)
[![codecov](https://codecov.io/gh/Criss-Wang/dpai/graph/badge.svg?token=D73VGZR7NN)](https://codecov.io/gh/Criss-Wang/dpai)
![GitHub License](https://img.shields.io/github/license/criss-wang/dpai)
[![commit](https://img.shields.io/github/last-commit/criss-wang/dpai)](https://github.com/criss-wang/dpai/commits/master)

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
4. Serve your model: run `deployaible serve --port=your_port`
   You will get a backend running on `your_port` (default is 9000). A sample endpoint will be `localhost:9000/your_model_name/predict`.
5. Test endpoint: run

```shell
curl -X POST -H "Content-Type: application/json" -d '{"data": ["val"]}' http://localhost:9100/GPT4/predict
```

6. You can also the APIs via swagger UI on `http://localhost:your_port/docs`

sample_notebook_placeholder

sample_architecture_placeholder


## Highlights

- Supports multiple types of model serving
- Sample UI
- Works on Linux/MacOS/Windows

## Install

[TODO] git instruction or pip install instruction

## Basic Usage

## Advanced Usage

## Misc

## Performance

## Documentation

[TODO] set up using [this link](https://docs.readthedocs.io/en/stable/intro/import-guide.html)

## Bugs/Requests

## License

## TODO's

1. `models.py` - `init` method needs to use model loader and allows torch/pickle/sklearn types
2. `model_manager.py` - enforce Singleton pattern with right locking mechanisms (also need to change the test case)

7. bugs: `AssertionError: write() before start_response` when go to predict page then go back
8. Celery component: add `try/except KeyboardInterrupt` as a potential fix to continuing celery worker
9. Kafka component: add APIs for submitting data to and listening result from kafka

- `python setup.py sdist`
- `twine upload dist/*`
