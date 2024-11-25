"""
最佳空调设计：
半径：0.25 m
高度：0.50 m
进风口数量：1
出风口数量：1
位置：(2.28, 4.00, 1.49)
"""

import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import random

# 房间和空调参数
r_w, r_l, r_h = 5, 8, 3  # 房间尺寸（米）
room_volume = r_w * r_l * r_h  # 房间体积（立方米）
max_ac_volume = 0.1  # 最大空调体积（立方米）
max_ac_power = 1800  # 最大空调功耗（瓦）
t_target = 24  # 室内目标温度（摄氏度）
t_ac_out = 24  # 空调出风口温度（摄氏度）
t_outdoor = 5  # 室外初始温度（摄氏度）

# 初始化温度场
nx, ny, nz = 40, 40, 20  # 网格点数 (x, y, z)
x = np.linspace(0, r_w, nx)
y = np.linspace(0, r_l, ny)
z = np.linspace(0, r_h, nz)
X, Y, Z = np.meshgrid(x, y, z)
T = np.full((nx, ny, nz), t_outdoor, dtype=float)

# 空调影响函数
def ac_influence(x, y, z, ac_pos, ac_radius):
    dist = np.sqrt((x - ac_pos[0]) ** 2 + (y - ac_pos[1]) ** 2 + (z - ac_pos[2]) ** 2)
    return np.exp(-dist ** 2 / (2 * ac_radius ** 2))

# 强制将个体的值限制在合法范围内
def repair_individual(individual):
    individual[0] = max(0.1, min(0.5, individual[0]))  # 半径范围
    individual[1] = max(0.5, min(1.5, individual[1]))  # 高度范围
    individual[2] = max(1, min(5, int(individual[2])))  # 进风口数量
    individual[3] = max(1, min(5, int(individual[3])))  # 出风口数量
    individual[4] = max(0, min(r_w, individual[4]))  # x位置范围
    individual[5] = max(0, min(r_l, individual[5]))  # y位置范围
    individual[6] = max(0, min(r_h, individual[6]))  # z位置范围
    return individual

# 适应度评估函数
def ac_design_evaluation(individual):
    r, h, n_in, n_out, x, y, z = repair_individual(individual)

    # 空调体积和功耗
    ac_volume = np.pi * r ** 2 * h
    if ac_volume > max_ac_volume:
        return 1e6,  # 惩罚无效设计
    ac_power = 50 * h + 30 * r + 10 * n_in + 10 * n_out
    if ac_power > max_ac_power:
        return 1e6,  # 惩罚功耗超限

    # 空调影响和温度场更新
    ac_pos = (x, y, z)
    influence = ac_influence(X, Y, Z, ac_pos, r)
    T_new = T + influence * (t_ac_out - T)

    # 计算温度偏差
    temperature_deviation = np.abs(T_new - t_target)
    fitness = np.sum(temperature_deviation)  # 温度偏差之和作为适应度
    return fitness,

# DEAP设置
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_r", random.uniform, 0.1, 0.25)  # 空调半径范围
toolbox.register("attr_h", random.uniform, 0.1, 2)  # 空调高度范围
toolbox.register("attr_n_in", random.randint, 1, 5)  # 进风口数量
toolbox.register("attr_n_out", random.randint, 1, 5)  # 出风口数量
toolbox.register("attr_x", random.uniform, 0, r_w)  # 空调位置x
toolbox.register("attr_y", random.uniform, 0, r_l)  # 空调位置y
toolbox.register("attr_z", random.uniform, 0, r_h)  # 空调位置z

toolbox.register("individual", tools.initCycle, creator.Individual,
                 (toolbox.attr_r, toolbox.attr_h, toolbox.attr_n_in, toolbox.attr_n_out,
                  toolbox.attr_x, toolbox.attr_y, toolbox.attr_z), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 遗传算法操作符
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.05, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", ac_design_evaluation)

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
                                           ngen=50,  # 代数
                                           stats=stats,
                                           halloffame=tools.HallOfFame(1),  # 存储最佳个体
                                           verbose=True)

# 提取最佳设计
best_individual = tools.selBest(population, 1)[0]
print("\n最佳空调设计：")
print(f"半径：{best_individual[0]:.2f} m")
print(f"高度：{best_individual[1]:.2f} m")
print(f"进风口数量：{int(best_individual[2])}")
print(f"出风口数量：{int(best_individual[3])}")
print(f"位置：({best_individual[4]:.2f}, {best_individual[5]:.2f}, {best_individual[6]:.2f})")

# 绘制优化过程
gens = logbook.select("gen")
min_fitness = logbook.select("min")
avg_fitness = logbook.select("avg")

plt.figure(figsize=(10, 6))
plt.plot(gens, min_fitness, label="Minimum Fitness")
plt.plot(gens, avg_fitness, label="Average Fitness")
plt.fill_between(gens,
                 np.array(avg_fitness) - np.array(logbook.select("std")),
                 np.array(avg_fitness) + np.array(logbook.select("std")),
                 alpha=0.2, label="Standard Deviation Range")
plt.xlabel("Generations")
plt.ylabel("Fitness (Temperature Deviation)")
plt.title("Air Conditioner Design Optimization Process")
plt.legend()  # 显示图例
plt.grid(True)  # 显示网格
plt.tight_layout()  # 调整布局

# 保存图像或显示
# plt.savefig("../figures/q1_ac_design_optimization_ga.png")
plt.show()