Adjust_para={
    "k":3,
    "step_dict":{
    "Qwen/Qwen2.5-Coder-1.5B-Instruct" : 1.63,
    "Qwen/Qwen2.5-Coder-7B-Instruct": 2.29,
    "deepseek-ai/deepseek-coder-1.3b-instruct" : 2.1,
    "deepseek-ai/deepseek-coder-6.7b-instruct" : 2.11
    ## More Model
    }
}


FIM={
    "Qwen/Qwen2.5-Coder-1.5B-Instruct":'''<|fim_prefix|><prefix>    if<|fim_suffix|><suffix><|fim_middle|>''',
    "Qwen/Qwen2.5-Coder-7B-Instruct":'''<|fim_prefix|><prefix>    if<|fim_suffix|><suffix><|fim_middle|>''',
    "deepseek-ai/deepseek-coder-1.3b-instruct":'''<｜fim▁begin｜><prefix>    if<｜fim▁hole｜>\n<suffix><｜fim▁end｜>''',
    "deepseek-ai/deepseek-coder-6.7b-instruct":'''<｜fim▁begin｜><prefix>    if<｜fim▁hole｜>\n<suffix><｜fim▁end｜>''',
    "bigcode/starcoder2-7b":'''<fim_prefix><prefix>    if<fim_suffix><suffix><fim_middle>'''
    ## More FIM temple
}