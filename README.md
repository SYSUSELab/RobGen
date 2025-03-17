## RobGen

Before testing RobGen, please configure the environment using conda first.

```
conda create -n Robcode python==3.9
conda activate Robcode
pip install tree_sitter
pip install tree_sitter_java
pip install transformers
pip install torch
```
#### Test RobGen
```
cd yourpath/RobGen

##If you want to use RobGen-Adj, run:
python Pipeline/generate.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct) --Adjust

##If you want to use RobGen-Ins, run:
python Pipeline/generate.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct) --Insert

##If you want to use RobGen-Adj+Ins, run:
python Pipeline/generate.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct) --Adjust --Insert

##run w/o RobGen:
python Pipeline/generate.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct)
```
