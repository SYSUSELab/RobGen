from util import stream_jsonl,write_jsonl
from transformers import AutoTokenizer,AutoModelForCausalLM
from pipeline import pipeline
from tqdm import tqdm
import json
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("model_name", type=str, help="Model name")
parser.add_argument("--Adjust", action="store_true", help="Use Adjust")
parser.add_argument("--Insert", action="store_true", help="Use Insert")
# 解析参数
args = parser.parse_args()

Adjust=args.Adjust
Insert=args.Insert

model_name=args.model_name
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
print("tokenizer over")
model =AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).to("cuda:0")
print("model over")

input_data={task["question_id"]: task["input"] for task in stream_jsonl("Pipeline/CEJavaHumanLabel.jsonl")}
signature_datas={task["question_id"]: task["signature"] for task in stream_jsonl("Pipeline/CEJavaHumanLabel.jsonl")}
datas = json.load(open("Pipeline/CoderEval4Java.json", encoding='utf-8'))
contexts={data["_id"]:json.loads(data["all_context"])["class_level"] for data in datas["RECORDS"]}



start=time.time()
write_jsonl(model_name.replace("/","-")+".jsonl", "")

for data in tqdm(datas["RECORDS"]) :
    id=data["_id"]
    input=input_data[id]
    context=contexts[id]
    signature_data=signature_datas[id]
    generate_result=pipeline(model_name,tokenizer,model,context,signature_data,input,Adjust,Insert)
    print(generate_result)
    sample=[dict(_id=id,generate_results=generate_result)]
    write_jsonl(model_name.replace("/","-")+".jsonl", sample,append=True)


end=time.time()
print("time: ",(end-start)/60,"min")
print("over")
    