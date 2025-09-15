import json
from util import stream_jsonl
from metric import count_try_catch_blocks,code_parser
ground_trues={data["id"]:data["code"]  for data in stream_jsonl("GT_code.jsonl")}
ids=ground_trues.keys()

    
for model in ["Qwen2.5-Coder-1.5B","Qwen2.5-Coder-7B","deepseek-coder-1.3b","deepseek-coder-6.7b"]:
    print("model: ",model)
    pass_num=0
    compile_num=0
    codes= {data["_id"]:data["generate_results"][0]["generate_code"] for data in stream_jsonl("Generate_data/"+model+"-Output.jsonl_out.jsonl")}
    passed={data["_id"]:data["generate_results"][0]["is_pass"] for data in stream_jsonl("Generate_data/"+model+"-Output.jsonl_out.jsonl")}
    errormessages={data["_id"]:data["generate_results"][0]["errormessage"] for data in stream_jsonl("Generate_data/"+model+"-Output.jsonl_out.jsonl")}
    rates={data["id"]:data["rate"] for data in stream_jsonl("GPT_Judger_Result/"+model+"_generate-data.jsonl")}
    # compile@1 and pass@1
    for id in ids:
        if(passed[id]):
            pass_num+=1
            compile_num+=1
        elif(errormessages[id]!="compile error"):
            compile_num+=1   
    print("Count of passed:{:d}".format(pass_num))
    print("Count of compiled success:{:d}".format(compile_num))
    print("Percentage of pass %:{:.2f}".format(pass_num/230))
    print("Percentage of compile %:{:.2f}".format(compile_num/230))
    # EHAR
    try_catch_count=0
    trues_try_catch_count=0
    count=0
    all=0
    for id in ids:
        Genflag=False
        GTflag=False
        if(not passed[id]):
            if(errormessages[id]=="compile error"):
                continue
        all+=1
        trues=ground_trues[id]
        code=codes[id]
        code_result=count_try_catch_blocks(code,"java")
        if(code_result["try"]!=0 or code_result["catch/except"]!=0):
            Genflag=True
            try_catch_count+=1
            

        trues_result=count_try_catch_blocks(trues,"java")
        if(trues_result["try"]!=0 or trues_result["catch/except"]!=0):
            GTflag=True
            trues_try_catch_count+=1
        if(Genflag and GTflag):
            count+=1
    print("Gen EHAR :{:.2f}".format(try_catch_count/all))
    print("GT EHAR:{:.3f}".format(trues_try_catch_count/all))
    
    # AvgABE
    ABE_num=0
    trues_ABE_num=0
    all=0
    for id in ids:
        if(not passed[id]):
            if(errormessages[id]=="compile error"):
                continue
        all+=1
        trues=ground_trues[id]
        code=codes[id]
        code_result=code_parser(code)
        ABE_num+=len(code_result)
        trues_result=code_parser(trues)
        trues_ABE_num+=len(trues_result)
    print("num of AvgABE :{:.2f}".format(ABE_num/all))
    
    # GPT judger result
    count1=0
    count2=0
    count3=0
    recall_list=[]
    for id in ids:
        if(not passed[id]):
            if(errormessages[id]=="compile error"):
                continue
        score=rates[id]
        if(score<3):
            count1+=1
        if(score==3 ):
            count2+=1
        if(score>3 ):
            count3+=1
    print("GT less than Gen:{:.2f}%".format(count1/(count1+count2+count3)*100))
    print("GT equal to Gen:{:.2f}%".format(count2/(count1+count2+count3)*100))
    print("GT better than Gen:{:.2f}%".format(count3/(count1+count2+count3)*100))
    print("----------------------------------------------------------------------------------------------")
    



















