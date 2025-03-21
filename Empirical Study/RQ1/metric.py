import tree_sitter_java as tsjava
from tree_sitter import Language, Parser
import re
parser = Parser(Language(tsjava.language()))


GUARD_CONDITIONS_JAVA = [
    r'\b\w+\s*(==|!=)\s*null\b',            
    r'\b\w+\.exists\(\)',                
    r'\b\w+\.can(Read|Write|Execute)\(\)',
    r'\b\w+\s*(==|!=|>|>=|<|<=)\s*\d+\b',  
    r'!\w+\.isEmpty\(\)|\b\w+\.length\(\)\s*>\s*0',  
    r'\b\w+\.size\(\)\s*>\s*0',          
]


def Unpack(node):
    while(node.grammar_name=="parenthesized_expression" or node.grammar_name=="unary_expression"):
        node=node.children[1]
    return node

def iscompare(node):
    text=bytes.decode(node.children[1].text)
    return text in ["<=",">=","==","!=","<",">"]

def unit_binary(node,list):
    node=Unpack(node)
    if(node.grammar_name=="binary_expression"):
        if(iscompare(node)):
            list.append(bytes.decode(node.text))
        text=bytes.decode(node.children[1].text)
        if(text in ["||","&&"]):
            list=unit_binary(node.children[0],list)
            list=unit_binary(node.children[2],list)  
        return list
    
    list.append(bytes.decode(node.text))
    return list
def relative_var(code):
    lines=code.split("\n")
    relative={}
    for line in lines:
        variable, value=extract_assignment(line)
        if(variable==None):
            continue
        relative[variable]= value
    return relative
def extract_assignment(java_code):
    pattern = r'^\s*\w+\s+(\w+)\s*=\s*(.*?);\s*$'  
    match = re.search(pattern, java_code)
    if match:
        variable = match.group(1)  
        value = match.group(2)  
        return variable, value
    pattern =r'^\s*(\w+)\s*=\s*(.+)\s*;'
    match = re.search(pattern, java_code)
    if match:
        variable = match.group(1)  
        value = match.group(2)  
        return variable, value
    return None, None
    


def traverse(node,list):
    pass_node=[]
    if(node.grammar_name=="if_statement" ):
        temp_node=Unpack(node.children[1])
        if(temp_node.grammar_name!="binary_expression"):
            list.append(bytes.decode(temp_node.text))
            pass_node.append(1)
            
    if(node.grammar_name=="while_statement" ):
        temp_node=Unpack(node.children[1])
        if(temp_node.grammar_name!="binary_expression"):
            list.append(bytes.decode(temp_node.text))
            pass_node.append(1)
    
    if(node.grammar_name=="for_statement"):
        temp_node=Unpack(node.children[3])
        if(temp_node.grammar_name!="binary_expression"):
            list.append(bytes.decode(temp_node.text))
            pass_node.append(3)

    if(node.grammar_name=="ternary_expression"):
        temp_node=Unpack(node.children[0])
        if(temp_node.grammar_name!="binary_expression"):
            list.append(bytes.decode(temp_node.text))
            pass_node.append(0)
        
    if(node.grammar_name=="binary_expression"):
        list=unit_binary(node,list)
        return list
    for i in range(len(node.children)):
       if(i not in pass_node):
            list=traverse(node.children[i],list)
    return list
import re

def parse_comparison_expression(expression):
    pattern = r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s+instanceof\s+([a-zA-Z_][a-zA-Z0-9_<>?,\s]*)\s*$'
    match = re.match(pattern, expression)
    if match:
        bound_variable, type_expression = match.groups()
        return [bound_variable]
    
    pattern = r'(.+?)\s*(==|!=|>=|<=|>|<)\s*(.+)'
    match = re.search(pattern, expression)
    constants = {"null", "true", "false"}
    if match:
        left_operand, operator, right_operand = match.groups()
        
        def is_variable(op):
            return (not re.match(r'^-?\d+(\.\d+)?$', op) and  
                    op.lower() not in constants and         
                    not re.match(r'^[\'\"].*[\'\"]$', op)   
                    and not re.match(r'^0[xX][0-9a-fA-F]+$', op)) 
        non_numeric_operands = [op for op in (left_operand, right_operand) if is_variable(op)]
        
        return  non_numeric_operands
    return [expression]



def code_parser(code):
    tree = parser.parse(bytes(code,"utf8"))
    cursor = tree.walk()
    list=traverse(cursor.node,[])
    return list

def RRI(generate_code,ground_true_code):
    gen=code_parser(generate_code)
    gt=code_parser(ground_true_code)
    gen_result=[]
    gt_result=[]
    for expression in gen:
        gen_result+=parse_comparison_expression(expression)

    relative=relative_var(generate_code)
    for i, var in  enumerate(gen_result):
        if(var in relative.keys()):
             gen_result[i]=relative[var]
    for expression in gt:
        gt_result+=parse_comparison_expression(expression)

    relative=relative_var(ground_true_code)
    for i, var in  enumerate(gt_result):
        if(var in relative.keys()):
             gt_result[i]=relative[var]
    gt=gt_result
    gen=gen_result
    if(len(gt)==0 and len(gen)!=0):
        return 1
    if(len(gt)==0 and len(gen)==0):
        return 0
    count=0
    temp=[i for i in gt]
    for i in gen:
        if(i in temp):
            temp.remove(i)
            count+=1
    a=1
    return (count+a*(len(gen)-count))/len(gt)-1
   
def BES(generate_code,ground_true_code):
    list=code_parser(generate_code)
    gt=code_parser(ground_true_code)
    list_result=[]
    gt_result=[]
    for expression in list:
        list_result+=parse_comparison_expression(expression)
    for expression in gt:
        gt_result+=parse_comparison_expression(expression)
    gt=gt_result
    list=list_result 
    if(len(gt)==0):
        return 1.0
    count=0
    temp=[i for i in gt]
    for i in list:
        if(i in temp):
            temp.remove(i)
            count+=1
    return count/len(gt)



def count_try_catch_blocks(code, language):
    if language.lower() == "python":
        try_pattern = r'\btry\b\s*:'
        catch_pattern = r'\bexcept\b'
    elif language.lower() == "java":
        try_pattern = r'\btry\b\s*\{'
        catch_pattern = r'\bcatch\b\s*\('
    else:
        return "Unsupported language"
    try_count = len(re.findall(try_pattern, code))
    catch_count = len(re.findall(catch_pattern, code))

    return {"try": try_count, "catch/except": catch_count}