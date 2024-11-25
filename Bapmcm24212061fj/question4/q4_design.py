"""
最佳三合一设备设计：
空调高度：0.2884 m，占比：60.00%
净化器高度：0.0961 m，占比：20.00%
加湿器高度：0.0961 m，占比：20.00%
设备总高度：0.4807 m
总容积：0.0944 m³（限制：0.1000 m³）
"""
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import random

# 参数设置
V_total_limit = 0.1  # 总容积限制，单位：立方米
D_Device = 0.5  # 设备直径（固定值），单位：米
radius = D_Device / 2  # 半径
A_cross_section = np.pi * radius**2  # 设备横截面积
target_ratios = [0.6, 0.2, 0.2]  # 空调、净化器、加湿器的初始占比

# 计算体积限制条件
max_heights = V_total_limit / A_cross_section  # 最大总高度限制

# 遗传算法适应度评估函数
def evaluate_heights(individual):
    ac_h, purifier_h, humidifier_h = individual
    total_volume = A_cross_section * (ac_h + purifier_h + humidifier_h)  # 计算总体积

    # 惩罚体积超限
    if total_volume > V_total_limit:
        return 1e6,

    # 偏离目标比例的罚值
    total_height = ac_h + purifier_h + humidifier_h
    actual_ratios = [ac_h / total_height, purifier_h / total_height, humidifier_h / total_height]
    deviation = np.sum((np.array(actual_ratios) - np.array(target_ratios))**2)  # 偏差平方和

    return deviation,  # 返回适应度值（越小越好）

# DEAP设置
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_height", random.uniform, 0.2 * max_heights, 0.5 * max_heights)  # 初始化随机高度
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_height, toolbox.attr_height, toolbox.attr_height), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.05, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate_heights)

# 初始化种群
population = toolbox.population(n=100)
# 添加统计跟踪
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)
# 遗传算法运行
population, logbook = algorithms.eaSimple(population, toolbox,
                                           cxpb=0.7, mutpb=0.2,
                                           ngen=50,  # 迭代次数
                                           stats=stats,
                                           halloffame=tools.HallOfFame(1),
                                           verbose=True)

# 提取最佳个体
best_individual = tools.selBest(population, 1)[0]
ac_h, purifier_h, humidifier_h = best_individual
total_height = ac_h + purifier_h + humidifier_h
actual_ratios = [ac_h / total_height, purifier_h / total_height, humidifier_h / total_height]

# 打印结果
print("\n最佳三合一设备设计：")
print(f"空调高度：{ac_h:.4f} m，占比：{actual_ratios[0]:.2%}")
print(f"净化器高度：{purifier_h:.4f} m，占比：{actual_ratios[1]:.2%}")
print(f"加湿器高度：{humidifier_h:.4f} m，占比：{actual_ratios[2]:.2%}")
print(f"设备总高度：{total_height:.4f} m")
print(f"总容积：{A_cross_section * total_height:.4f} m³（限制：{V_total_limit:.4f} m³）")

# 提取适应度数据
gens = logbook.select("gen")
max_deviation = logbook.select("max")
min_deviation = logbook.select("min")
avg_deviation = logbook.select("avg")
std_deviation = logbook.select("std")
# 适应度（偏差）变化过程图
plt.figure(figsize=(10, 6))
# plt.plot(gens, max_deviation, color="red", label="MAX Deviation")
plt.plot(gens, min_deviation, color="blue", label="MIN Deviation")
plt.plot(gens, avg_deviation, color="orange", label="AVG Deviation")
plt.fill_between(gens,
                 np.array(avg_deviation) - np.array(std_deviation),
                 np.array(avg_deviation) + np.array(std_deviation),
                 alpha=0.2, label="Standard deviation range")
plt.xlabel("Generation")
plt.ylabel("Deviation (Fitness)")
plt.title("Fitness (Deviation) Optimization Process")
plt.legend()
plt.grid(True)
plt.tight_layout()
# 保存或显示适应度变化图
# plt.savefig("../figures/q4_fitness_optimization_process.png")
plt.show()

# 创建一个新的图像，用于绘制三合一产品设计
fig, ax = plt.subplots(figsize=(5, 10))

# 绘制加湿器部分，放置在顶部
humidifier = plt.Rectangle((0, total_height - humidifier_h), D_Device, humidifier_h, color='lightblue', label='Humidifier')
ax.add_patch(humidifier)
ax.text(D_Device / 2, total_height - humidifier_h / 2, f'Humidifier\n{humidifier_h:.2f} m', ha='center', va='center')

# 绘制空调部分，放置在中部
ac = plt.Rectangle((0, total_height - humidifier_h - ac_h), D_Device, ac_h, color='lightcoral', label='Air Conditioner')
ax.add_patch(ac)
ax.text(D_Device / 2, total_height - humidifier_h - ac_h / 2, f'Air Conditioner\n{ac_h:.2f} m', ha='center', va='center')

# 绘制空气净化器部分，放置在底部
purifier = plt.Rectangle((0, 0), D_Device, purifier_h, color='lightgreen', label='Air Purifier')
ax.add_patch(purifier)
ax.text(D_Device / 2, purifier_h / 2, f'Air Purifier\n{purifier_h:.2f} m', ha='center', va='center')

# 设置图形参数
ax.set_xlim(0, D_Device)
ax.set_ylim(0, total_height)
ax.set_xticks([])
ax.set_ylabel('Height (m)')
ax.set_title('The Three-in-One Product (Front View)')

# 显示网格
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()
plt.tight_layout()
# 保存或显示三合一产品设计图
# plt.savefig('../figures/q4_The_three_in_one_product.png', dpi=400)
plt.show()