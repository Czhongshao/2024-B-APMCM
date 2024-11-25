"""
最优增湿器设计：
半径：0.18 米
高度：1.00 米
位置：(3.10, 3.45, 2.16)
增湿率：4.48
"""
import numpy as np
from pyswarm import pso
import matplotlib.pyplot as plt

# 房间的宽、长、高
r_w, r_l, r_h = 5, 8, 3
max_volume = 0.1  # 最大增湿器体积
target_humidity_diff = 0.5  # 湿度差(0.4-0.6)
air_velocity = 8.0  # 空气流速
# 存储优化过程的可视化数据
iteration_data = []

# PSO的目标函数
def humidifier_objective(x):
    global iteration_data  # 用于存储进度
    r, h, x_pos, y_pos, z_pos = x

    # 体积限制
    volume = np.pi * r ** 2 * h
    if volume > max_volume:
        return 1e6  # 对无效设计进行惩罚

    # 表面积和增湿率
    surface_area = 2 * np.pi * r * h
    humidity_effect = -surface_area * air_velocity * target_humidity_diff  # 需要最大化（负值）

    # 追加可视化数据
    iteration_data.append((r, h, x_pos, y_pos, z_pos, -humidity_effect))

    return humidity_effect

# [r, h, x, y, z]的界限
bounds = [
    (0.1, 0.5),  # r
    (0.1, 1.0),  # h
    (0, r_w),  # x
    (0, r_l),  # y
    (0, r_h),  # z
]

# 运行PSO
best_position, best_value = pso(humidifier_objective, lb=[b[0] for b in bounds], ub=[b[1] for b in bounds],
                                 swarmsize=50, maxiter=50)

# 提取迭代和性能数据
iterations = range(1, len(iteration_data) + 1)
fitness_values = [data[5] for data in iteration_data]

# 绘制优化过程
plt.figure(figsize=(10, 6))
plt.plot(iterations, fitness_values, label='Fitness over Iterations')
plt.xlabel('Iteration')
plt.ylabel('Fitness Value (Humidification Rate)')
plt.title('Particle Swarm Optimization Progress')
plt.grid()
plt.legend()
plt.tight_layout()
# plt.savefig("../figures/q3_weet_pso.png")
plt.show()

# 结果
print("\n最优增湿器设计：")
print(f"半径：{best_position[0]:.2f} 米")
print(f"高度：{best_position[1]:.2f} 米")
print(f"位置：({best_position[2]:.2f}, {best_position[3]:.2f}, {best_position[4]:.2f})")
print(f"增湿率：{-best_value:.2f}")