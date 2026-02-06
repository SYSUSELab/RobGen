## RobGen

Before testing RobGen, please configure the environment using conda first.

```
conda create -n Robcode python==3.9
conda activate Robcode
pip install tree_sitter
pip install tree_sitter_java
pip install transformers
pip install torch
pip install peft
```
#### Test RobGen
```
cd yourpath/RobGen/Framework

##If you want to use RobGen, run:
python RobGen_generate.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct) --RobGen

```
#### Baseline
```
cd yourpath/RobGen/Framework

##If you want to use RobGen w/o Checker, run:
python RobGen_generate.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct) --Adjust

##run w/o RobGen(Greedy Sampling):
python RobGen_generate.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct)

##run Robust_Coder_Prompt(RP):
python Robust_Coder_Prompt.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct) 

```
#### RobEval
All data of the RobEval is stored in the ```RobEval``` directory.
If you need to use RobEval, first create the CoderEval test container, place file "RobEval.jsonl" and file "JavaExec_RobEval.py" under the path "/home/travis/builds/java" , and then execute:
```
python JavaExec_RobEval.py (codes_result_to_test.jsonl) 1 
```
#### Empirical Study
All data for the Empirical Study is stored in the ```Empirical Study``` directory.