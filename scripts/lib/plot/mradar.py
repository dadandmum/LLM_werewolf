import numpy as np
import matplotlib.pyplot as plt
from math import pi


def draw_radar(input):

    with open(input,"r") as f:
        data=f.read()
        
    lines=data.splitlines()
    
    
    value_labels = lines[0].split(',')[1:]
    value_labels=value_labels[:-1]
    value_labels=np.array(value_labels)
    
    values_dict=dict()
    set_labels=[]
    y_min=999
    y_max=0
    for i in range(1,len(lines),1):
        line = lines[i]
        items=line.split(',')
        items=items[:-1]
        
        label=items[0]
        values=[float(x) for x in items[1:]]
        y_min=min(y_min,np.min(values))
        y_max=max(y_max,np.max(values))
        values_dict[label]=values
        set_labels.append(label)
    
    # plt.style.use('ggplot')
        
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(value_labels), endpoint=False).tolist()
    angles += angles[:1]

    # 创建颜色列表
    colors = ['m', 'r', 'b', 'orange', 'm']
    
    # 创建子图
    fig, axs = plt.subplots(figsize=(10, 10), nrows=2, ncols=2, subplot_kw=dict(polar=True))
    # 调整子图间距
    fig.subplots_adjust(wspace=0.33, hspace=0.33, top=0.95, bottom=0.05)
    
    
    # 绘制雷达图
    for t in range(4):
        values_c=np.array(values_dict[set_labels[t+1]])
        values=np.array(values_dict[set_labels[0]])
        r = int(t / 2)
        c = int(t % 2)
        ax = axs[r][c]
        color=colors[t]
        
        # 闭合图形
        values = np.concatenate((values,[values[0]]))
        values_c = np.concatenate((values_c,[values_c[0]]))
        
        
        # 绘制第0组数据
        ax.plot(angles, values, color='grey', linewidth=2, linestyle='dashed', label=set_labels[0])
        ax.fill(angles, values, color='grey', alpha=0.25)

        # 绘制比较的数据组
        ax.plot(angles, values_c, color=color, linewidth=2, label=set_labels[t+1])
        ax.fill(angles, values_c, color=color, alpha=0.1)

        # 设置标签
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(value_labels,fontsize=18, fontname='Arial')
        
        ax.set_yticks(np.arange(np.floor(y_min),np.ceil(y_max),2))
        ax.set_ylim(np.floor(y_min),np.ceil(y_max))
        
        ax.set_title(set_labels[t+1], y=1.08 , fontsize=22,fontname='Arial')
        ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.2))
    

    # 显示图形
    # plt.show()
    
    # 保存
    plt.savefig("output.jpg" , dpi=300, format='jpg')
    
draw_radar("data.cvs")