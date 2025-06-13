import json

# Minimal YAML stub for tests when PyYAML is unavailable

def dump(data, stream=None):
    text = json.dumps(data)
    if stream is None:
        return text
    stream.write(text)


def safe_load(stream):
    if isinstance(stream, str):
        return json.loads(stream)
    return json.load(stream)
