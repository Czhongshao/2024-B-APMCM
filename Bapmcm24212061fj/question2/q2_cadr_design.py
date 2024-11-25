"""
最佳净化器设计：
直径 D = 0.24 m
高度 H = 1.9 m
滤网层数 N_filter = 8
进风口数量 N_in = 2
出风口数量 N_out = 4
最佳 CADR = 576.00 m³/h
"""
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import random

# 房间和净化器参数
r_w, r_l, r_h = 5, 8, 3  # 房间尺寸（米）
ROOM_VOLUME = r_w * r_l * r_h  # 房间体积（立方米）
DEVICE_VOLUME = 0.1  # 净化器最大体积（立方米）
MAX_FLOW = 600  # 最大气流量（立方米/小时）
MAX_POWER = 1800  # 最大功耗（瓦特）
K_FILTER = 0.8  # 过滤器效率常数

# 净化器设计的适应度评估函数
def air_purifier_design(individual):
    D, H = individual[0], individual[1]  # 直径和高度
    N_filter, N_in, N_out = int(individual[2]), int(individual[3]), int(individual[4])

    # 体积约束
    volume = np.pi * (D / 2)**2 * H
    if volume > DEVICE_VOLUME:
        return (0,)  # 惩罚无效设计

    # 计算滤网面积和流量
    filter_area = np.pi * D * H * N_filter
    Q_in = min(N_in * (MAX_FLOW / 2), MAX_FLOW)  # 总进风量
    Q_out = min(N_out * (MAX_FLOW / 2), MAX_FLOW)  # 总出风量

    # 效率模型
    air_change_rate = Q_in / ROOM_VOLUME
    eta = 1 - np.exp(-K_FILTER * filter_area * air_change_rate)

    # CADR计算
    cadr = Q_out * eta

    # 功耗约束
    power_consumption = 50 + 100 * N_filter + 100 * N_in + 100 * N_out
    if power_consumption > MAX_POWER:
        return (0,)  # 惩罚超功耗设计

    return (cadr,)  # 返回CADR作为适应度

# DEAP设置
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_D", random.uniform, 0.1, 0.5)  # 直径
toolbox.register("attr_H", random.uniform, 0.5, 1.5)  # 高度
toolbox.register("attr_filter", random.randint, 1, 5)  # 滤网层数
toolbox.register("attr_inlet", random.randint, 1, 3)  # 进风口数量
toolbox.register("attr_outlet", random.randint, 1, 3)  # 出风口数量

# 个体和种群初始化
toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_D, toolbox.attr_H, toolbox.attr_filter,
                  toolbox.attr_inlet, toolbox.attr_outlet), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 遗传算法操作符
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.05, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", air_purifier_design)

# 初始化种群
population = toolbox.population(n=100)

# 添加统计跟踪
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("std", np.std)
stats.register("min", np.min)
stats.register("max", np.max)

# 运行遗传算法
population, logbook = algorithms.eaSimple(population, toolbox,
                                          cxpb=0.7, mutpb=0.2,
                                          ngen=50,  # 代数
                                          stats=stats,
                                          halloffame=tools.HallOfFame(1),  # 存储最佳个体
                                          verbose=True)

# 提取所有个体的CADR值并计算平均值
cadr_values = [ind.fitness.values[0] for ind in population]
avg_cadr = np.mean(cadr_values)

# 输出最佳设计（以平均 CADR 为准）
best_individual = tools.selBest(population, 1)[0]
print("\n最佳净化器设计：")
print(f"直径 D = {best_individual[0]:.2f} m")
print(f"高度 H = {best_individual[1]:.2f} m")
print(f"滤网层数 N_filter = {int(best_individual[2])}")
print(f"进风口数量 N_in = {int(best_individual[3])}")
print(f"出风口数量 N_out = {int(best_individual[4])}")
print(f"最佳 CADR = {avg_cadr:.2f} m³/h")  # 输出平均 CADR

# 绘制优化过程
gens = logbook.select("gen")
max_cadr = logbook.select("max")
min_cadr = logbook.select("min")
avg_cadr_log = logbook.select("avg")

plt.figure(figsize=(10, 6))
plt.plot(gens, max_cadr, color="red", label="MAX CADR")
plt.plot(gens, min_cadr, color="blue", label="MIN CADR")
plt.plot(gens, avg_cadr_log, color="orange", label="AVG CADR")
plt.fill_between(gens,
                 np.array(avg_cadr_log) - np.array(logbook.select("std")),
                 np.array(avg_cadr_log) + np.array(logbook.select("std")),
                 alpha=0.2, label="Standard deviation range")
plt.xlabel("Generation")
plt.ylabel("CADR (m³/h)")
plt.title("CADR optimization process")
plt.legend()
plt.grid(True)
plt.tight_layout()
# plt.savefig("../figures/q2_CADR_optimization_process.png")
plt.show()
