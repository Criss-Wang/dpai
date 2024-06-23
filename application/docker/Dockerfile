FROM python:3.8

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

ARG PIP_EXTRA_INDEX_URL

ENV HAYSTACK_TELEMETRY_ENABLED False
ENV NLTK_DATA=/home/app_name/nltk_data
# The sentence transformers models are stored in this directory
ENV SENTENCE_TRANSFORMERS_HOME=/home/app_name/models
# The cross-encoder models are stored in this directory
ENV TRANSFORMERS_CACHE=/home/app_name/models

ENV PATH="/home/app_name/.local/bin:$PATH"

USER username
WORKDIR /app

RUN mkdir -p /app \
    && mkdir -p $NLTK_DATA  \
    && mkdir -p $TRANSFORMERS_CACHE

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt


RUN python -m nltk.downloader words stopwords punkt \
    && python -c "from sentence_transformers import SentenceTransformer; model=SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-dot-v1');"

COPY . /app

RUN pip install -e . --no-cache-dir --no-deps

# run any additional setup scripts before entrypoint
RUN python -m app.some_setup

ENTRYPOINT ["entrypoints/services/run_service.sh"]
