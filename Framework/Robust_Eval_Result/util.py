import json 
import os
from typing import Iterable,Dict
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

def folder_split(dependency_path):
    code=""
    with open(dependency_path,"r") as f:
        for line in f.readlines():
            code+=line
    root_node = parser.parse(bytes(code,encoding="utf-8")).root_node
    import_and_expression=""
    split_unit={}
    comment=""
    for child in root_node.children:
        if(child.grammar_name=="comment"):
            comment+=child.text.decode(encoding="utf-8")+"\n"

        if(child.grammar_name=="import_statement" or child.grammar_name=="if_statement" or child.grammar_name=="import_from_statement"or child.grammar_name=="expression_statement"):
            import_and_expression+=comment+child.text.decode(encoding="utf-8")+"\n"
            comment=""

        if(child.grammar_name=="class_definition"):
            node=child
            class_name=node.children[1].text.decode(encoding="utf-8")
            ##保存class声明和其注释
            split_unit[class_name]=("class",node.text.decode(encoding="utf-8"),comment+node.text.decode(encoding="utf-8").split("\n")[0])
            comment=""

        if(child.grammar_name=="function_definition"):
            node=child
            function_name=node.children[1].text.decode(encoding="utf-8")
            split_unit[function_name]=("function",comment+node.text.decode(encoding="utf-8"))
            comment=""

        if(child.grammar_name=="decorated_definition"):
            decorate=comment
            node=child.children[0]
            while(node.grammar_name!="class_definition" and node.grammar_name!="function_definition"):
                decorate+=(node.text.decode(encoding="utf-8"))
                node=node.next_sibling
            if(node.children[0].text.decode(encoding="utf-8")=="class"):
                class_name=node.children[1].text.decode(encoding="utf-8")
                split_unit[class_name]=("class",node.text.decode(encoding="utf-8"),decorate+"\n"+node.text.decode(encoding="utf-8").split("\n")[0])
            if(node.children[0].text.decode(encoding="utf-8")=="def"):
                function_name=node.children[1].text.decode(encoding="utf-8")
                split_unit[function_name]=("function",decorate+"\n"+node.text.decode(encoding="utf-8"))
            comment=""
    
    split_unit["import_and_expression"]=import_and_expression
    return split_unit

def function_in_class(class_code):
    split_unit={}
    node=parser.parse(bytes(class_code,encoding="utf-8")).root_node.children[0]
    ###找到class内部定义
    for child in node.children:
        if(child.grammar_name=="block"):
            node=child
    comment=""
    import_and_expression=""
    for child in node.children:
        if(child.grammar_name=="comment"):
            comment+="    "+child.text.decode(encoding="utf-8")+"\n"

        if(child.grammar_name=="import_statement" or child.grammar_name=="if_statement" or child.grammar_name=="import_from_statement" or child.grammar_name=="expression_statement"):
            import_and_expression+=comment+"    "+child.text.decode(encoding="utf-8")+"\n"
            comment=""

        if(child.grammar_name=="function_definition"):
            node=child
            function_name=node.children[1].text.decode(encoding="utf-8")
            split_unit[function_name]=("function",comment+"    "+node.text.decode(encoding="utf-8"))
            comment=""

        if(child.grammar_name=="decorated_definition"):
            decorate=comment
            node=child.children[0]
            while(node.grammar_name!="function_definition"):
                decorate+=("    "+node.text.decode(encoding="utf-8"))
                node=node.next_sibling
            function_name=node.children[1].text.decode(encoding="utf-8")
            split_unit[function_name]=("function",decorate+"\n"+"    "+node.text.decode(encoding="utf-8"))
            comment=""
    
    split_unit["import_and_expression"]=import_and_expression
    return split_unit


# 将依赖解析为路径，并分析出依赖的类名和类中成员名/依赖文件中的元素名
def parser_path(project_name,completion_path,dependency):
    completion_path=completion_path[:-3].split("/")
    while(completion_path[-1]!=project_name):
        completion_path=completion_path[:-1]
    path_prefix="/".join(completion_path[:-1])
    dependency=dependency.split(".")
    in_file=[]
    while(not os.path.exists(path_prefix+"/"+"/".join(dependency)+".py")):
        try:
            if(os.path.exists(path_prefix+"/"+"/".join(dependency)+"/__init__.py")):
                dependency_path=path_prefix+"/"+"/".join(dependency)+"/__init__.py"
                dependency_class=None
                dependency_element=None
                if(len(in_file)==1):
                    dependency_element=in_file[-1]
                if(len(in_file)==2):
                    dependency_class=in_file[-1]
                    dependency_element=in_file[-2]
                return dependency_path,dependency_class,dependency_element
            in_file.append(dependency[-1])
            dependency=dependency[:-1]
        except:
            print("在该项目中，不存在该依赖")
            return None,None,None
    dependency_path=path_prefix+"/"+"/".join(dependency)+".py"
    dependency_class=None
    dependency_element=None
    if(len(in_file)==1):
        dependency_element=in_file[-1]
    if(len(in_file)==2):
        dependency_class=in_file[-1]
        dependency_element=in_file[-2]
    return dependency_path,dependency_class,dependency_element




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