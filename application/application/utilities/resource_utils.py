import json
from cachetools import cached


@cached(cache={})
def get_resource():
    with open("resources/sample.json") as f:
        resource_mapping = json.load(f)
    return resource_mapping
