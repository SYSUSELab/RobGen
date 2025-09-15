### Notice
1. All model-generated code is stored in JSONL files within the ```Generate_data``` directory, containing task IDs and the generated code.
2. All GPT-4o evaluation results are stored under the ```GPT_Judger_Result``` directory. Here, "code" refers to the generated code being evaluated, and "text" refers to the evaluation output provided by the GPT-4o.
3. All metrics defined in the articles are implemented in ```metric.py```.
4. Running ```RQ1.py``` will display the evaluation results of the model-generated code.
5. Running ```GPT-judger_result_draw.py``` will show the distribution of GPT-4o evaluation results between the model-generated code and the reference code.