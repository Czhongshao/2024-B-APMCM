import numpy as np
import matplotlib.pyplot as plt

# 房间尺寸
r_w, r_l, r_h = 5, 8, 3  # 房间的宽、长、高 (米)

# 初始湿度参数
initial_humidity = 0.2  # 初始房间湿度 (单位: 相对湿度, 0.2 即 20%)
target_humidity = 0.6  # 目标湿度
humidifier_strength = 0.05  # 加湿器的单位湿度增量

# 加湿器位置和尺寸
humidifier_position = (3.10, 3.45, 2.16)  # x, y, z
humidifier_radius = 0.18  # 优化后的加湿器半径 (米)
humidifier_height = 1.00  # 优化后的加湿器高度 (米)
radius = 1 # 作用半径

# 网格划分
nx, ny, nz = 40, 40, 30  # 网格分辨率 (x, y, z)
x = np.linspace(0, r_w, nx)
y = np.linspace(0, r_l, ny)
z = np.linspace(0, r_h, nz)
X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

# 初始化湿度场
humidity = np.full((nx, ny, nz), initial_humidity, dtype=float)

# 加湿器影响区域函数 (基于高斯分布)
def humidifier_influence(x, y, z, position, radius):
    dist = np.sqrt((x - position[0])**2 + (y - position[1])**2 + (z - position[2])**2)
    return np.exp(-dist**2 / (2 * radius**2))

# 设置模拟参数
time_steps = 3000  # 模拟时间步数
dt = 0.1  # 时间步长 (秒)
print(f"当前运行时间是{time_steps * dt}s")
diffusion_coeff = 2.4e-5  # 湿度扩散系数 (单位: m^2/s) 标准大气压,24℃的情况下

# 开始模拟湿度扩散
for t in range(time_steps):
    influence = humidifier_influence(X, Y, Z, humidifier_position, humidifier_radius + radius)
    humidity += influence * humidifier_strength * dt  # 加湿器增加湿度
    # 使用拉普拉斯算子计算湿度的扩散效应
    laplacian_x = (np.roll(humidity, 1, axis=0) + np.roll(humidity, -1, axis=0) - 2 * humidity) / (x[1] - x[0])**2
    laplacian_y = (np.roll(humidity, 1, axis=1) + np.roll(humidity, -1, axis=1) - 2 * humidity) / (y[1] - y[0])**2
    laplacian_z = (np.roll(humidity, 1, axis=2) + np.roll(humidity, -1, axis=2) - 2 * humidity) / (z[1] - z[0])**2
    laplacian = laplacian_x + laplacian_y + laplacian_z
    humidity += diffusion_coeff * laplacian * dt  # 更新湿度分布
    # 限制湿度在合理范围内
    humidity = np.clip(humidity, initial_humidity, target_humidity)

    # 墙壁不穿透，初始湿度，确保墙体为绝热且湿度不穿透
    humidity[0, :, :] = humidity[-1, :, :] = humidity[:, 0, :] = humidity[:, -1, :] = humidity[:, :, 0] = humidity[:, :, -1] = initial_humidity


# 模拟结束后评估达到目标湿度的散点占比
reached_target = (humidity >= target_humidity).sum()
total_points = nx * ny * nz
proportion_reached_target = reached_target / total_points

print(f"达到目标湿度的散点占比为: {proportion_reached_target:.2%}")
# 模拟结束后计算平均湿度值
average_humidity = np.mean(humidity)

print(f"模拟结束后房间内的平均湿度值为: {average_humidity:.2f}")

# # 可视化
# # fig = plt.figure(figsize=(16, 8))
# # ax1 = fig.add_subplot(121)
#
# # cross_section 是湿度场的一个切片，它的大小应为 (room_length, room_width)
# cross_section = humidity[:, :, nz // 2]  # 中间高度的横截面
# fig1 = plt.figure()
# ax1 = fig1.add_subplot()
# # 由于房间的长和宽在横截面上对应，x和y的尺寸应与cross_section的形状一致
# im = ax1.contourf(x, y, cross_section.T, levels=20, cmap='Blues')  # .T 转置数据
# plt.colorbar(im, ax=ax1)
# ax1.set_title('Humidity Distribution (Middle Cross-section)')
# ax1.set_xlabel('Width/m')
# ax1.set_ylabel('Length/m')
# plt.tight_layout()
# # plt.savefig(f'../figures/q3_humidity_diff_{time_steps * dt}s.png')
#
# # 加湿器湿度影响 3D 散点图
# fig2 = plt.figure()
# ax2 = fig2.add_subplot(projection='3d')
# # 计算湿度影响
# humidifier_influence_plot = humidifier_influence(X, Y, Z, humidifier_position, humidifier_radius)
# # 将湿度影响作为颜色映射
# humidity_values = np.clip(humidity, initial_humidity, target_humidity)
# # 绘制3D散点图，湿度值决定点的颜色
# sc = ax2.scatter(X.ravel(), Y.ravel(), Z.ravel(), c=humidity_values.ravel(), cmap='Blues', alpha=0.2, s=1.5)
# # 设置标题和坐标轴标签
# ax2.set_title('Humidity Distribution and Humidifier Influence')
# ax2.set_xlabel('Width/m')
# ax2.set_ylabel('Length/m')
# ax2.set_zlabel('Height/m')
# # 添加颜色条
# # plt.colorbar(sc, ax=ax2, label='Humidity Level')
#
# plt.tight_layout()
# # plt.savefig(f'../figures/q3_humidity_scatter_{time_steps * dt}s.png')
# # plt.savefig(f'../figures/q3_humidity_influence_{time_steps * dt}s.png')
# # plt.show()
