import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
class_dict={
    1:"Missing Null Checks",
    2:"Missing Specific Value Checks",
    3:"Missing Range Checks",
    4:"Missing Boolean Value Checks",
    5:"Missing Type Checks on Variables",
    6:"Missing Assertions",
    7:"Missing Error Handling ",
    8:"Errorous Expression",
    9:"Inconsistent Expression"

}
fig, axs = plt.subplots(2,2, figsize=(36,16))

datas=json.load(open("classification/Qwen2.5-Coder-1.5B-Instruct.json","r",encoding="utf-8"))["datas"]
result={}
for i in range(1,10):
   result[i]=0
count=0
for data in datas:
    count+=1
    for type in data["type_id"]:
        result[type]+=1


result = dict(sorted(result.items(),key = lambda x:x[1],reverse = False))

all=sum(result.values())
for k, v in result.items():
    result[k]/=all
    result[k]=round(result[k]*100, 2)
print(result)

categories = [str(k) for k in result.keys()]
values = [v for v in result.values()]
titles = [ class_dict[key]for key in result.keys()] 

cmap = cm.get_cmap("Blues", len(values))
colors = cmap(np.linspace(0.45, 0.9, len(categories))) 

bars = axs[0,0].barh(categories, values, color=colors,height=0.8,edgecolor="black")
threshold=15
right_edge = axs[0,0].get_xlim()[1] 
left_edge=axs[0,0].get_xlim()[0] 
for bar, title, value in zip(bars, titles, values):
    xval = bar.get_width()  
    yval = bar.get_y() + bar.get_height()*0.78

    if xval > threshold:  
        axs[0,0].text(left_edge +0.5, yval, title, 
                 va='top', ha='left', color='white', fontsize=25, fontweight='bold',style='italic', family='Times New Roman')

        axs[0,0].text(xval + 1.4, yval, f"{value}"+"%", 
                 va='top', ha='right', color='black', fontsize=18, fontweight='bold',style='italic', family='Times New Roman')

    else:  

        axs[0,0].text(xval + 0.5, yval, f"{value}"+"%", 
                 va='top', ha='left', color='black', fontsize=18, fontweight='bold',style='italic', family='Times New Roman')


        axs[0,0].text(right_edge - 0.5, yval, title, 
                 va='top', ha='right', color='black', fontsize=25, fontweight='bold',style='italic', family='Times New Roman')
axs[0,0].set_xticks([])
axs[0,0].set_yticks([])
axs[0,0].set_xlabel('(a) Qwen2.5-Coder-1.5B', fontsize=20, fontweight='bold', style='italic', family='Times New Roman')










datas=json.load(open("classification/deepseek-coder-1.3b-instruct.json","r",encoding="utf-8"))["datas"]
result={}
for i in range(1,10):
   result[i]=0
count=0
for data in datas:
    count+=1
    for type in data["type_id"]:
        result[type]+=1


result = dict(sorted(result.items(),key = lambda x:x[1],reverse = False))

all=sum(result.values())
for k, v in result.items():
    result[k]/=all
    result[k]=round(result[k]*100, 2)

categories = [str(k) for k in result.keys()]
values = [v for v in result.values()]


bars = axs[0,1].barh(categories, values, color=colors,height=0.8,edgecolor="black")
threshold=15
right_edge = axs[0,1].get_xlim()[1] 
left_edge=axs[0,1].get_xlim()[0] 
for bar, title, value in zip(bars, titles, values):
    xval = bar.get_width()  
    yval = bar.get_y() + bar.get_height()*0.78

    if xval > threshold:  

        axs[0,1].text(left_edge +0.5, yval, title, 
                 va='top', ha='left', color='white', fontsize=25, fontweight='bold',style='italic', family='Times New Roman')
        

        axs[0,1].text(xval + 1.5, yval, f"{value}"+"%", 
                 va='top', ha='right', color='black', fontsize=18, fontweight='bold',style='italic', family='Times New Roman')

    else:  

        axs[0,1].text(xval + 0.5, yval, f"{value}"+"%", 
                 va='top', ha='left', color='black', fontsize=18, fontweight='bold',style='italic', family='Times New Roman')


        axs[0,1].text(right_edge - 0.5, yval, title, 
                 va='top', ha='right', color='black', fontsize=25, fontweight='bold',style='italic', family='Times New Roman')
axs[0,1].set_xticks([])
axs[0,1].set_yticks([])
axs[0,1].set_xlabel('(c) DeepseekCoder-1.3B', fontsize=20, fontweight='bold', style='italic', family='Times New Roman')




datas=json.load(open("classification/Qwen2.5-Coder-7B-Instruct.json","r",encoding="utf-8"))["datas"]
result={}
for i in range(1,10):
   result[i]=0
count=0
for data in datas:
    count+=1
    for type in data["type_id"]:
        result[type]+=1
result = dict(sorted(result.items(),key = lambda x:x[1],reverse = False))

all=sum(result.values())
for k, v in result.items():
    result[k]/=all
    result[k]=round(result[k]*100, 2)

categories = [str(k) for k in result.keys()]
values = [v for v in result.values()]
titles = [ class_dict[key]for key in result.keys()]  


bars = axs[1,0].barh(categories, values, color=colors,height=0.8,edgecolor="black")
threshold=15
right_edge = axs[1,0].get_xlim()[1] 
left_edge=axs[1,0].get_xlim()[0] 
for bar, title, value in zip(bars, titles, values):
    xval = bar.get_width()  
    yval = bar.get_y() + bar.get_height()*0.78

    if xval > threshold:  

        axs[1,0].text(left_edge +0.5, yval, title, 
                 va='top', ha='left', color='white', fontsize=25, fontweight='bold',style='italic', family='Times New Roman')
        

        axs[1,0].text(xval + 1.3, yval, f"{value}"+"%", 
                 va='top', ha='right', color='black', fontsize=18, fontweight='bold',style='italic', family='Times New Roman')

    else:  

        axs[1,0].text(xval + 0.5, yval, f"{value}"+"%", 
                 va='top', ha='left', color='black', fontsize=18, fontweight='bold',style='italic', family='Times New Roman')

        axs[1,0].text(right_edge - 0.5, yval, title, 
                 va='top', ha='right', color='black', fontsize=25, fontweight='bold',style='italic', family='Times New Roman')
axs[1,0].set_xticks([])
axs[1,0].set_yticks([])
axs[1,0].set_xlabel('(b) Qwen2.5-Coder-7B', fontsize=20, fontweight='bold', style='italic', family='Times New Roman')



datas=json.load(open("classification/deepseek-coder-6.7b-instruct.json","r",encoding="utf-8"))["datas"]
result={}
for i in range(1,10):
   result[i]=0
count=0
for data in datas:
    count+=1
    for type in data["type_id"]:
        result[type]+=1

result = dict(sorted(result.items(),key = lambda x:x[1],reverse = False))

all=sum(result.values())
for k, v in result.items():
    result[k]/=all
    result[k]=round(result[k]*100, 2)

categories = [str(k) for k in result.keys()]
values = [v for v in result.values()]


bars = axs[1,1].barh(categories, values, color=colors,height=0.8,edgecolor="black")
threshold=15
right_edge = axs[1,1].get_xlim()[1] 
left_edge=axs[1,1].get_xlim()[0] 
for bar, title, value in zip(bars, titles, values):
    xval = bar.get_width()  
    yval = bar.get_y() + bar.get_height()*0.78
    if xval > threshold:  

        axs[1,1].text(left_edge +0.5, yval, title, 
                 va='top', ha='left', color='white', fontsize=25, fontweight='bold',style='italic', family='Times New Roman')
        

        axs[1,1].text(xval + 1.4, yval, f"{value}"+"%", 
                 va='top', ha='right', color='black', fontsize=18, fontweight='bold',style='italic', family='Times New Roman')

    else:  
        axs[1,1].text(xval + 0.5, yval, f"{value}"+"%", 
                 va='top', ha='left', color='black', fontsize=18, fontweight='bold',style='italic', family='Times New Roman')
        axs[1,1].text(right_edge - 0.5, yval, title, 
                 va='top', ha='right', color='black', fontsize=25, fontweight='bold',style='italic', family='Times New Roman')
axs[1,1].set_xticks([])
axs[1,1].set_yticks([])
axs[1,1].set_xlabel('(d) DeepseekCoder-6.7B', fontsize=20, fontweight='bold', style='italic', family='Times New Roman')



plt.tight_layout()
plt.show()