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

##If you want to use Robust_Coder_Prompt(RP), run:
python Robust_Coder_Prompt.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct) 

##If you want to use Post_Generation_Insertion(PGI), run:
python Post_Generation_Insertion.py model_name(e.g.Qwen/Qwen2.5-Coder-1.5B-Instruct) 

```
#### Empirical Study
All data for the Empirical Study is stored in the ```Empirical Study``` directory.