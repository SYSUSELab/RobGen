import torch
from transformers.generation.logits_process import LogitsProcessor, LogitsProcessorList
from util import clean
from config import Adjust_para 
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSequenceClassification
from peft import PeftModel
import re
PROMPT='''/**The contexts can be used when generate :
<CONTEXT> **/
<INPUT>
'''
device="cuda:0"
Checker_model_name = "Qwen/Qwen3-0.6B"
lora_path = "sft-Qwen3-0.6B-ckpt"  
Checker_tokenizer = AutoTokenizer.from_pretrained(Checker_model_name)
if Checker_tokenizer.pad_token is None:
    Checker_tokenizer.pad_token = Checker_tokenizer.eos_token 
print("Checker tokenizer over")
Checker_model=PeftModel.from_pretrained(AutoModelForSequenceClassification.from_pretrained(
    Checker_model_name,
    num_labels=2,
), lora_path).to(device)
Checker_model.config.pad_token_id = Checker_tokenizer.pad_token_id
Checker_model.eval()
print("Checker model over")
def checker(code): 
    input_ids = Checker_tokenizer(code, return_tensors="pt").to(Checker_model.device)
    with torch.no_grad():
        outputs =Checker_model(**input_ids)
    # prob= torch.softmax(outputs.logits[0], dim=-1)
    pred = outputs.logits.argmax(axis=-1)
    return pred.item()==1
class Adjust_logits_processor(LogitsProcessor):
    def __init__(self,k,tokenizer,signature,context_len,step):
        self.k=k
        self.tokenizer=tokenizer
        self.signature=signature
        self.context_len=context_len
        self.step=step
        self.adjust=False
    def __call__(self,sequences: torch.LongTensor,scores: torch.FloatTensor) -> torch.FloatTensor:
        token_ids =torch.argsort(scores[0],0,descending=True)[0:self.k].tolist()
        if(sequences[0].shape[0]==self.context_len ):
            if(checker(self.signature+"\n"+self.tokenizer.decode(sequences[0][self.context_len:]))):
                self.adjust=True
                return scores
        elif("\n" in self.tokenizer.decode(token_ids[0])):
            if(checker(self.signature+"\n"+self.tokenizer.decode(sequences[0][self.context_len:]))):
                self.adjust=True
                return scores
        if(self.adjust):
            #pass whitespaces
            if(not set(self.tokenizer.decode(token_ids[0])).issubset({" ", "\t"})):
                relative_rank=0
                for token_id in token_ids[0:self.k]:
                    token=self.tokenizer.decode(token_id)
                    if("if"== "".join(token.split())):
                        scores[0][token_id]+=relative_rank*self.step
                        break
                    relative_rank+=1
                self.adjust=False
                return scores
        
        return scores

    


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

def RobGen_pipeline(model_name,tokenizer,model,context,signature_data,input):
    prompt=PROMPT
    input=prompt.replace("<CONTEXT>", context).replace("<INPUT>",input)
    context_len=tokenizer(input, return_tensors="pt")["input_ids"].shape[1]
    logits_processor=LogitsProcessorList()
    k=Adjust_para["k"]
    step_dict=Adjust_para["step_dict"]
    if(model_name in Adjust_para["step_dict"].keys()):
        step=step_dict[model_name]
    else:
        step=1.0
    logits_processor.append(Adjust_logits_processor(k,tokenizer,signature_data,context_len,step))
    print("-------------------------------------RobGen------------------------------------------")
    generate_result=signature_data+"\n"+Adjust_generate_one_completion(tokenizer,model,input,logits_processor)
   

    code=clean(generate_result)
    return code


