import torch
from transformers.generation.logits_process import LogitsProcessor, LogitsProcessorList
from util import clean
from config import Adjust_para

PROMPT='''/**The contexts can be used when generate :
<CONTEXT> **/
<INPUT>
'''


class Adjust_logits_processor(LogitsProcessor):
    def __init__(self,k,tokenizer,step):
        self.k=k
        self.tokenizer=tokenizer
        self.step=step
    def __call__(self,sequences: torch.LongTensor,scores: torch.FloatTensor) -> torch.FloatTensor:
        token_ids =torch.argsort(scores[0],0,descending=True)[0:self.k].tolist()
        #pass whitespaces
        relative_rank=0
        if(self.tokenizer.decode(token_ids[0]).replace(" ","")==""):
            return scores
        for token_id in token_ids[0:self.k]:
            token=self.tokenizer.decode(token_id)
            if("if"== token.replace(" ","")):
                scores[0][token_id]+=relative_rank*self.step
                break
            relative_rank+=1
        return scores
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

def Adjust_generate_one_completion(tokenizer,model,input,logits_processor):
    input = tokenizer(input, return_tensors="pt").to(model.device)
    generated_dict = model.generate(**input,max_new_tokens=1024,
                                    return_dict_in_generate=True,
                                    return_legacy_cache=False,
                                    output_scores = False,
                                    logits_processor=logits_processor,
                                    do_sample=False
                                    )
    generated_ids=generated_dict.sequences[0]
    filling=tokenizer.decode(generated_ids[input["input_ids"].shape[1]:], skip_special_tokens = True)
    return (filling)

def Adj_pipeline(model_name,tokenizer,model,context,signature_data,input):
    prompt=PROMPT
    input=prompt.replace("<CONTEXT>", context).replace("<INPUT>",input)
    logits_processor=LogitsProcessorList()
    k=Adjust_para["k"]
    step_dict=Adjust_para["step_dict"]
    if(model_name in Adjust_para["step_dict"].keys()):
        step=step_dict[model_name]
    else:
        step=1.0
    logits_processor.append(Adjust_logits_processor(k,tokenizer,step))
    print("-------------------------------------Adjust------------------------------------------")
    generate_result=signature_data+"\n"+Adjust_generate_one_completion(tokenizer,model,input,logits_processor)
    

    code=clean(generate_result)
    
    return code
def GS_pipeline(tokenizer,model,context,signature_data,input):
    prompt=PROMPT
    input=prompt.replace("<CONTEXT>", context).replace("<INPUT>",input)
    print("----------------------------------Greedy Sampling---------------------------------------")
    generate_result=signature_data+"\n"+generate_one_completion(tokenizer,model,input)
    code=clean(generate_result)
    return code