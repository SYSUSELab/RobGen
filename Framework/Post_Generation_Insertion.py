import torch
from util import clean,is_comment,M3_clean
from config import FIM
import re
from util import stream_jsonl,write_jsonl
from transformers import AutoTokenizer,AutoModelForCausalLM
from tqdm import tqdm
import json


PROMPT='''/**The contexts can be used when generate :
<CONTEXT> **/
<INPUT>
'''

INSERT_PROMPT = '''/**The contexts can be used when generate :
<CONTEXT> **/
'''

def generate_one_completion(tokenizer,model,input):
    input = tokenizer(input, return_tensors="pt").to(model.device)
    generated_dict = model.generate(**input,max_new_tokens=1024,
                                    return_dict_in_generate=True,
                                    return_legacy_cache=False,
                                    output_scores = False,
                                    do_sample=False
                                    )
    generated_ids=generated_dict.sequences[0]
    filling=tokenizer.decode(generated_ids[input["input_ids"].shape[1]:], skip_special_tokens = True)
    return (filling)



def pipeline(model_name,tokenizer,model,context,signature_data,input):
    prompt=PROMPT
    input=prompt.replace("<CONTEXT>", context).replace("<INPUT>",input)
    generate_result=signature_data+"\n"+generate_one_completion(tokenizer,model,input)
    code=clean(generate_result)
    lines=code.split("\n")
    start_line_index=1
    while(is_comment(lines[start_line_index])):
        start_line_index+=1
    pattern = r"^\s*if\s*\("
    if(not re.match(pattern, lines[start_line_index])):  
        if (model_name in FIM.keys()):
            FIM_prompt=FIM[model_name]
        else:
            raise(model_name+"'s FIM template is not configured")
        prefix=lines[0]+"\n"
        suffix="\n".join(lines[start_line_index:])
        input=FIM_prompt.replace("<prefix>",INSERT_PROMPT+prefix).replace("<suffix>",suffix).replace("<CONTEXT>",context)
        generate_result="    "+M3_clean("    if"+generate_one_completion(tokenizer,model,input))
        code=prefix+generate_result+"\n"+suffix
        code=clean(code)
    return code



import argparse

parser = argparse.ArgumentParser()
parser.add_argument("model_name", type=str, help="Model name/path")



args = parser.parse_args()




model_name=args.model_name

model_path=""+model_name
tokenizer = AutoTokenizer.from_pretrained(model_path)

print("tokenizer over")
model =AutoModelForCausalLM.from_pretrained(model_path).to("cuda:3")
print("model over")

input_data={task["question_id"]: task["input"] for task in stream_jsonl("CEJavaHumanLabel.jsonl")}
signature_datas={task["question_id"]: task["signature"] for task in stream_jsonl("CEJavaHumanLabel.jsonl")}
datas = json.load(open("Pipeline/CoderEval4Java.json", encoding='utf-8'))
contexts={data["_id"]:json.loads(data["all_context"])["class_level"] for data in datas["RECORDS"]}



write_jsonl(model_name.replace("/","-")+"_PGI.jsonl", "")

for data in tqdm(datas["RECORDS"]) :
    id=data["_id"]
    input=input_data[id]
    context=contexts[id]
    signature_data=signature_datas[id]
    generate_result=pipeline(model_name,tokenizer,model,context,signature_data,input)
    sample=[dict(_id=id,generate_results=generate_result)]
    write_jsonl(model_name.replace("/","-")+"_PGI.jsonl", "", sample,append=True)