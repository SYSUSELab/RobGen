from transformers import AutoTokenizer, AutoModelForCausalLM
import csv
from tqdm import tqdm
import torch
import numpy as np
import json 
from typing import Iterable,Dict
import os
import tree_sitter_java as tsjava
from tree_sitter import Language, Parser
from util import stream_jsonl,write_jsonl,clean
PROMPT = '''/** When generating code, pay attention to the following points:
1.Validate the input to check all external inputs and ensure that the program receives legitimate and expected inputs.
2.Perform boundary checks to ensure that arrays, lists, or other data structures are not accessed out of bounds.
3.Capture and handle runtime errors through appropriate error handling or exception handling. Pay attention to situations where error handling can manage the issue, and avoid throwing exceptions if possible.
**/
/**The contexts can be used when generate :
<CONTEXT> **/
<INPUT>
'''
def generate_one_completion(input):
    input_ids = tokenizer(input, return_tensors="pt")["input_ids"].to(model.device)
    generated_dict = model.generate(input_ids,max_new_tokens= 1024,
                                    return_dict_in_generate=True,
                                    return_legacy_cache=False,
                                    do_sample=False,
                                    pad_token_id=tokenizer.pad_token_id,
                                    output_scores = False)
    generated_ids=generated_dict.sequences[0]
    filling=tokenizer.decode(generated_ids[input_ids.shape[1]:], skip_special_tokens = True)
    return (filling)


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("model_name", type=str, help="Model name/path")



args = parser.parse_args()




model_name=args.model_name

model_path=""+model_name
tokenizer = AutoTokenizer.from_pretrained(model_path)

print("tokenizer over")
model =AutoModelForCausalLM.from_pretrained(model_path).to("cuda:0")
print("model over")

input_data={task["question_id"]: task["input"] for task in stream_jsonl("CEJavaHumanLabel.jsonl")}
signature_data={task["question_id"]: task["signature"] for task in stream_jsonl("CEJavaHumanLabel.jsonl")}
datas = json.load(open('CoderEval4Java.json', encoding='utf-8'))
contexts={data["_id"]:json.loads(data["all_context"])["class_level"] for data in datas["RECORDS"]}




write_jsonl(model_name.replace("/","-")+"_generate_RP.jsonl", "",append=False)
for id in tqdm(contexts.keys()):
    input=input_data[id]
    context=contexts[id]
    input=PROMPT.replace("<CONTEXT>", context).replace("<INPUT>",input)
    generate_result=generate_one_completion(input)
    generate_result=clean(signature_data[id]+"\n"+generate_result)
    print(generate_result)
    sample=[dict(_id=id,generate_results=[generate_result])]
    write_jsonl(model_name.replace("/","-")+"_generate_RP.jsonl", sample,append=True)
    






    


