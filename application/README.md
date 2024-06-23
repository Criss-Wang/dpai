## What is it?

It is a REST service that provides an answer to a user's query It is to be able to compose an answer
to a user request/search from a set of relevant documents using LLM. Check the confluece page for
more details, and the architecture diagram.

## Design Diagram

## How to run it?

### Prerequisites

### Python Installation

Ensure Python 3.8 is installed on your machine. Check your Python version by running:

```bash
python --version
```

### Virtual Environment

Set up and activate a virtual environment with the following commands:

```bash
virtualenv -p python3.8 venv
. ./venv/bin/activate
```

### Installing Dependencies

To install required packages for the project, execute:

```bash
pip install -r requirements.txt
```

To install main packages for the project, execute:

```bash
pip install -e .
```

### Configuration File Setup

Duplicate the `.env.sample` file and name it as `.env` using the following command.

```bash
cp .env.sample .env
```

Export the environment variables:

```bash
export $(grep -v '^#' .env | xargs -0)
```

### VPN and kubectl Configuration

Connect to your VPN and configure kubectl for the desired environment:

```bash
kubectx <dev_cluster>
kubens <dev_env_name>
```

## Running the Services

### Port Forwarding

Before running any rag, make sure to port-forward the required services:

 ```bash
kubectl port-forward SERVICE_NAME PORT_NUMBER &
```

### Verify indexes with


### Run the service using FastAPI

```bash
python entrypoints/mains/service.py
```

#### Trigger an execution

In browser, go to the following url

```bash
http://localhost:8000/docs
```

For the swagger documentation and testing the service with sample requests.


### Run the service using gRPC

```bash
application services run-grpc --port 50052
```

#### Use Postman

Publish to localhost:50052
