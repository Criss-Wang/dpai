![build](https://github.com/criss-wang/dpai/workflows/build/badge.svg) 
![docs](https://github.com/criss-wang/dpai/workflows/docs/badge.svg) 
![lint](https://github.com/criss-wang/dpai/workflows/lint/badge.svg)
[![codecov](https://codecov.io/gh/Criss-Wang/dpai/graph/badge.svg?token=D73VGZR7NN)](https://codecov.io/gh/Criss-Wang/dpai)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![commit](https://img.shields.io/github/last-commit/criss-wang/dpai)](https://github.com/criss-wang/dpai/commits/master)

## Introduction
Deployable AI aims to enable quick inference serving in local environment in various styles of your choice.

## Getting Started
### Installation
To install this package, the easiest is to run `pip install dpai`. If you prefer directly install using this repo code, you can clone it and run `make` command directly. 

### Basic Usage
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

3. Register model: run `deployaible register --name=your_model_name --model_path=your_model_path --inference_path=your_inference_path`
4. Serve your model: run `deployaible serve --port=your_port`
   You will get a backend running on `your_port` (default is 9000). A sample endpoint will be `localhost:9000/your_model_name/predict`.
5. Format your data input in JSON style: `{"data": your_input_data}`. Make sure it aligns with the `input_fn` your infrence script
6. Test endpoint: example request

    ```shell
    curl -X POST -H "Content-Type: application/json" -d '{"data": ["val"]}' http://localhost:9100/GPT4/predict
    ```

6. You can also the APIs via swagger UI on `http://localhost:your_port/docs`

### Sample notebook


## Highlights
- Supports multiple types of model serving
- Sample UI
- Works on Linux/MacOS/Windows


## Limitations
- Currently only supported request type is `application/json`.

## Documentation
See the doc [here](https://dpai.readthedocs.io/)
