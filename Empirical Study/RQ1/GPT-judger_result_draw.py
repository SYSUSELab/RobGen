
import numpy as np
import matplotlib.pyplot as plt
lable=['Generated Underperforms Human', 'Generated ≈ Human', 'Generated Outperforms Human']
bar_width = 0.1
x = np.arange(len(lable)) 
deepseek_small=[41.83,41.83,16.34]
deepseek_big=[38.15,46.24,15.61]
qwen_small=[38.96,42.21,18.83]
qwen_big=[28.49,48.26,23.26]
plt.bar(x - 1.5*bar_width, deepseek_small, width=bar_width, label='DeepSeekCoder-1.3B')
plt.bar(x - 0.5*bar_width, deepseek_big, width=bar_width, label='DeepSeekCoder-6.7B')
plt.bar(x + 0.5*bar_width, qwen_small, width=bar_width, label='Qwen2.5-Coder-1.5B' )
plt.bar(x + 1.5*bar_width, qwen_big, width=bar_width, label='Qwen2.5-Coder-7B' )
plt.ylabel('Percentage',fontweight='bold',fontsize=10)
plt.xticks(x, lable,fontweight='bold', fontsize=12)

plt.legend(['DeepSeekCoder-1.3B','DeepSeekCoder-6.7B', 'Qwen2.5-Coder-1.5B', 'Qwen2.5-Coder-7B'], 
           loc='upper right', bbox_to_anchor=(1, 1),fontsize=8,prop={'weight': 'bold'},
           markerscale=0.8,  
           handlelength=1.5)

plt.tight_layout()  
plt.savefig("RQ1.pdf", format="pdf")