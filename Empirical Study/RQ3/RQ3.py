import json
import matplotlib.pyplot as plt
import numpy as np
dict_list=[]
for model in ["Qwen2.5-Coder-1.5B-Instruct","Qwen2.5-Coder-7B-Instruct","deepseek-coder-1.3b-instruct","deepseek-coder-6.7b-instruct"]:
    position={data["id"]:data["pos"] for data in json.load(open("Position/"+model+".json",encoding="utf-8"))["datas"]}
    pos_dict={}
    for id,pos in position.items():
        if(pos in pos_dict.keys()):
            pos_dict[pos]+=1
        else:
            pos_dict[pos]=1
    dict_list.append(pos_dict)
dict1=dict_list[0]
dict2=dict_list[1]
dict3=dict_list[2]
dict4=dict_list[3]

for i in range(1,17):
    if(i not in dict1):
        dict1[i]=0
    if(i not in dict2):
        dict2[i]=0
    if(i not in dict3):
        dict3[i]=0
    if(i not in dict4):
        dict4[i]=0
dict1=dict(sorted(dict1.items()))
dict2=dict(sorted(dict2.items()))
dict3=dict(sorted(dict3.items()))
dict4=dict(sorted(dict4.items()))



categories = [i for i in range(1,16)]+[">15"]
values1 = [v /sum(dict1.values())*100 for v in dict1.values()]
values2 = [v /sum(dict2.values())*100 for v in dict2.values()]
values3 = [v /sum(dict3.values())*100 for v in dict3.values()]
values4 = [v /sum(dict4.values())*100 for v in dict4.values()]
bar_width = 0.2
index = np.arange(1,17)
plt.bar(index-1.5*bar_width, values1, bar_width, label='Qwen2.5-Coder-1.5B')
plt.bar(index-bar_width/2, values2, bar_width, label='Qwen2.5-Coder-7B')
plt.bar(index+bar_width/2 , values3, bar_width, label='DeepSeekCoder-1.3B')
plt.bar(index + 1.5*bar_width, values4, bar_width, label='DeepSeekCoder-6.7B')

plt.xlabel('position')
plt.ylabel('percentage %')


plt.xticks(index, categories)


plt.legend()

plt.savefig("RQ3.pdf", format="pdf")
