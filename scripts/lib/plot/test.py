import numpy as np
import matplotlib.pyplot as plt

# 假设这是你的数据
values = [
    [5, 10, 15, 20, 25],  # 第0组数据
    [3, 8, 10, 15, 20],   # 第1组数据
    [4, 7, 12, 18, 22],   # 第2组数据
    [6, 9, 14, 19, 24],   # 第3组数据
    [2, 6, 11, 16, 21],   # 第4组数据
]

# 类别标签
labels = np.array(['A', 'B', 'C', 'D', 'E'])
num_vars = len(labels)

# 计算角度
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

# 创建颜色列表
colors = ['b', 'g', 'r', 'c', 'm']

# 创建子图
fig, axs = plt.subplots(figsize=(10, 10), nrows=2, ncols=2, subplot_kw=dict(polar=True))

# 调整子图间距
fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

# 绘制雷达图
for ax, color in zip(axs.ravel(), colors):
    # 获取要比较的数据组
    data_to_compare = values.pop(1)
    data = values[0]  # 第0组数据

    # 闭合数据
    data += data[:1]
    data_to_compare += data_to_compare[:1]

    # 绘制第0组数据
    ax.plot(angles, data, color=color, linewidth=2, label='Group 0')
    ax.fill(angles, data, color=color, alpha=0.25)

    # 绘制比较的数据组
    ax.plot(angles, data_to_compare, color='k', linewidth=2, linestyle='dashed', label='Compare Group')
    ax.fill(angles, data_to_compare, color='k', alpha=0.1)

    # 设置标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

# 为每个子图设置标题
titles = ['Comparison 1', 'Comparison 2', 'Comparison 3', 'Comparison 4']
for ax, title in zip(axs.ravel(), titles):
    ax.set_title(title, y=1.08)

# 显示图例
for ax in axs.ravel():
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.2))

# 显示图形
plt.show()