import matplotlib.pyplot as plt
import numpy as np
import json
dict_list=[]
for model in ["Qwen2.5-Coder-1.5B-Instruct","Qwen2.5-Coder-7B-Instruct","deepseek-coder-1.3b-instruct","deepseek-coder-6.7b-instruct"]:
    rankings={data["id"]:data["ranking"] for data in json.load(open("Ranking/"+model+".json",encoding="utf-8"))["datas"]}
    ranking_dict={}
    for id,ranking in rankings.items():
        if(ranking in ranking_dict.keys()):
            ranking_dict[ranking]+=1
        else:
            ranking_dict[ranking]=1
    dict_list.append(ranking_dict)

for dicts in dict_list:
    print(dicts)

dict1=dict_list[0]
dict2=dict_list[1]
dict3=dict_list[2]
dict4=dict_list[3]

for i in range(2,32):
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

categories = [i for i in range(2,31)]+[">30"]
values1 = [v /sum(dict1.values())*100 for v in dict1.values()]
values2 = [v /sum(dict2.values())*100 for v in dict2.values()]
values3 = [v /sum(dict3.values())*100 for v in dict3.values()]
values4 = [v /sum(dict4.values())*100 for v in dict4.values()]

bar_width = 0.2

index = np.arange(2,32)

plt.bar(index-1.5*bar_width, values1, bar_width, label='Qwen2.5-Coder-1.5B')
plt.bar(index-bar_width/2, values2, bar_width, label='Qwen2.5-Coder-7B')
plt.bar(index+bar_width/2 , values3, bar_width, label='DeepSeekCoder-1.3B')
plt.bar(index + 1.5*bar_width, values4, bar_width, label='DeepSeekCoder-6.7B')

plt.xlabel('ranking')
plt.ylabel('percentage %')


plt.xticks(index, categories)


plt.legend()

plt.show()