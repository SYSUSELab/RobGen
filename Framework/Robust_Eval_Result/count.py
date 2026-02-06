from util import stream_jsonl
method="PGI"
models=["deepseek-coder-1.3b","deepseek-coder-6.7b","Qwen2.5-Coder-1.5B","Qwen2.5-Coder-7B","starcoder2-7b"]
methods=["GS","RobGen","RobGen_without_Checker","RP"]

for method in methods:
    scores=[]
    for model in models:
        set_count=0
        pass_count=0
        rob_datas={data["_id"]:data["generate_results"][0]["is_pass"]for data in  stream_jsonl(method+"/"+model+"-Output.jsonl_out_rob.jsonl")}
        for data in  stream_jsonl("../Generated_Result/"+method+"/"+model+"-Output.jsonl_out.jsonl"):
            if(data["generate_results"][0]["is_pass"] ):
                set_count+=1
                if(data["_id"] in rob_datas.keys() ):
                    if(rob_datas[data["_id"]]):
                        pass_count+=1
                else:
                    set_count-=1
        scores.append(pass_count/set_count*100)
        print(f"model:{model} , score:{round(pass_count/set_count*100,1)}")
    print(f"method:{method} , avg score:{round(sum(scores)/len(scores),1)}")
    print("\n"+"-"*20)

