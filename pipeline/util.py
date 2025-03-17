import json 
import os
from typing import Iterable,Dict
import tree_sitter_java as tsjava
from tree_sitter import Language, Parser

def is_comment(line):
    line = line.strip()
    if line.startswith("//"):
        return True
    if line.startswith("/*") or line.startswith("/**"):
        return True
    if line.endswith("*/"):
        return True
    return False


def clean(code):
    LANGUAGE = Language(tsjava.language())
    parser = Parser(LANGUAGE)
    cursor = parser.parse(bytes(code,"utf8")).walk()
    if(cursor.node.children[0].grammar_name=="method_declaration"):
        result=bytes.decode(cursor.node.children[0].text,"utf8")
        return result
    return code
def M3_clean(code):
    LANGUAGE = Language(tsjava.language())
    parser = Parser(LANGUAGE)
    cursor = parser.parse(bytes(code,"utf8")).walk()
    node=cursor.node
    return bytes.decode(node.children[0].text,"utf8")
def stream_jsonl(filename: str) -> Iterable[Dict]:
    with open(filename, "r") as fp:
            for line in fp:
                if any(not x.isspace() for x in line):
                    yield json.loads(line)

def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False):
    if append:
        mode = 'ab'
    else:
        mode = 'wb'
    filename = os.path.expanduser(filename)
    with open(filename, mode) as fp:
        for x in data:
            fp.write((json.dumps(x) + "\n").encode('utf-8'))