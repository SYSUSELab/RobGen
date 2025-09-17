from util import stream_jsonl,write_jsonl
from transformers import AutoTokenizer,AutoModelForCausalLM
from RobGen_pipeline import RobGen_pipeline
from Adjust_pipeline import Adj_pipeline,GS_pipeline
from tqdm import tqdm
import json
import argparse

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


parser = argparse.ArgumentParser()
parser.add_argument("model_name", type=str, help="Model name")
parser.add_argument("--RobGen", action="store_true", help="Use RobGen")
parser.add_argument("--Adjust", action="store_true", help="Use RobGen w/o Checker")

# 解析参数
args = parser.parse_args()
RobGen=args.RobGen
Adjust=args.Adjust
if(RobGen):
    suffix="_RobGen"
elif(Adjust):
    suffix="_Adj"
else:
    suffix=""

model_name=args.model_name
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
print("tokenizer over")
model =AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to("cuda:0")
print("model over")

input_data={task["question_id"]: task["input"] for task in stream_jsonl("CEJavaHumanLabel.jsonl")}
signature_datas={task["question_id"]: task["signature"] for task in stream_jsonl("CEJavaHumanLabel.jsonl")}
datas = json.load(open("CoderEval4Java.json", encoding='utf-8'))
contexts={data["_id"]:json.loads(data["all_context"])["class_level"] for data in datas["RECORDS"]}




write_jsonl(model_name.replace("/","-")+suffix+".jsonl", "")

for data in tqdm(datas["RECORDS"]) :
    id=data["_id"]
    input=input_data[id]
    context=contexts[id]
    signature_data=signature_datas[id]
    if(RobGen):
        generate_result=RobGen_pipeline(model_name,tokenizer,model,context,signature_data,input)
    elif(Adjust):
        generate_result=Adj_pipeline(model_name,tokenizer,model,context,signature_data,input)
    else:
        generate_result=GS_pipeline(tokenizer,model,context,signature_data,input)
    sample=[dict(_id=id,generate_results=generate_result)]
    write_jsonl(model_name.replace("/","-")+suffix+".jsonl", sample,append=True)


print("over")
    
