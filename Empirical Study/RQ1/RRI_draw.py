
import numpy as np
import matplotlib.pyplot as plt
lable=["RRI<0","RRI=0","RRI>0"]
bar_width = 0.1
x = np.arange(len(lable)) 
deepseek_small=[52.3,35.95,11.76]
deepseek_big=[47.67,40.7,11.63]
qwen_small=[45.81,38.71,15.48]
qwen_big=[33.92,49.71,16.37]
plt.bar(x - 1.5*bar_width, deepseek_small, width=bar_width, label='DeepSeekCoder-1.3B')
plt.bar(x - 0.5*bar_width, deepseek_big, width=bar_width, label='DeepSeekCoder-6.7B')
plt.bar(x + 0.5*bar_width, qwen_small, width=bar_width, label='Qwen2.5-Coder-1.5B' )
plt.bar(x + 1.5*bar_width, qwen_big, width=bar_width, label='Qwen2.5-Coder-7B' )
plt.ylabel('Percentage',fontweight='bold',fontsize=10)
plt.xticks(x, lable,fontweight='bold', fontsize=8)

plt.legend(['DeepSeekCoder-1.3B','DeepSeekCoder-6.7B', 'Qwen2.5-Coder-1.5B', 'Qwen2.5-Coder-7B'], 
           loc='upper right', bbox_to_anchor=(1, 1),fontsize=8,prop={'weight': 'bold'},
           markerscale=0.8,  
           handlelength=1.5)

plt.tight_layout()  
plt.show()