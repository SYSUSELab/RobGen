from openai import OpenAI
from tqdm import tqdm
from util import stream_jsonl,write_jsonl
prompt='''You are a software architecture expert. Please carefully evaluate and compare the robustness of the following {LANGUAGE} code A and B based on specific robustness criteria that are critical to practical software development and architectural design.
Begin your assessment with a brief explanation that addresses the key factors listed below. Following your explanation, assign a rating to the codes on a scale from 1 to 5, where 1 indicates the code A has the lowest robustness than code B and 5 indicates the code A has the highest robustness than code B.3 indicates the code A's robustness equals to code B. Please adhere strictly to the following format for your rating: “Rating: [[X]]”, where X is your rating. 

Criteria for Evaluation:
* Input Boundary Defense:
-  All  data originating from external sources must be validated to ensure it conforms to the expected format and value range.
- All subroutines(functions/methods) must validate their input parameters for boundaries and legality.
-  For any detected invalid input, a clear handling strategy must be defined.
* Assertion Mechanism:
- Use assertions to handle errors that should never occur。
- Avoid placing executable subroutines inside assertions。
* Error Handling:
- When handling errors, continue execution and simply return a harmless value。
- Return an error status code and invoke an error-handling subroutine or object。
* Exception Handling:
- Use exceptions only when other coding practices cannot address the issue。
- Avoid throwing exceptions when error handling can adequately resolve the issue.
- Avoid using empty catch statements。

After your analysis, provide your explanation for the aspects evaluated. Then, conclude with the rating in the specified format. For example, if you rate the code A has the highest robustness than code B, you should write: “Rating: [[5]]”. {LANGUAGE} code A to be assessed: {CONTENTA}.
{LANGUAGE} code B to be assessed: {CONTENTB}.'''

Gen_path="deepseek-coder-1.3b-Output.jsonl_out.jsonl" 
Gen_data={data["_id"]:data for data in stream_jsonl("Generate_data/"+Gen_path)}


client = OpenAI(
    api_key = "",
    base_url = "https://api.agicto.cn/v1"
)

for data in tqdm(stream_jsonl("/home/lisum/robust_compare/GT_code.jsonl")):
    for i in range(3):
        import random
        num = random.choice([0, 1])
        if(num==1):
            codeA=data["code"]
            codeB=Gen_data[data["id"]]["generate_results"][0]["generate_code"]
        else:
            codeA=Gen_data[data["id"]]["generate_results"][0]["generate_code"]
            codeB=data["code"]
        chat_completion = client.chat.completions.create(    
            messages=[
                {            
                    "role": "user",            
                    "content": prompt.replace("{LANGUAGE}","Java").replace("{CONTENTA}",codeA).replace("{CONTENTB}",codeB),        
                }   
            ],    
            model="gpt-4o",
        )
        rate=chat_completion.choices[0].message.content
        write_jsonl(Gen_path.relpace("Output.jsonl_out","rate"),[{"id":data["id"],"num":num,"rate":rate}],append=True)

        
    

