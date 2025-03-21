import json
from typing import Iterable,Dict
import os

def stream_jsonl(filename: str) -> Iterable[Dict]:
    with open(filename, "r") as fp:
            for line in fp:
                if any(not x.isspace() for x in line):
                    yield json.loads(line)

def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False):
    """
    Writes an iterable of dictionaries to jsonl
    """
    if append:
        mode = 'ab'
    else:
        mode = 'wb'
    filename = os.path.expanduser(filename)
    with open(filename, mode) as fp:
        for x in data:
            fp.write((json.dumps(x) + "\n").encode('utf-8'))