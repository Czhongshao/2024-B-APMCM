import numpy as np
import matplotlib.pyplot as plt

# 房间尺寸与环境参数
r_w = 5   # 室内宽度（米）
r_l = 8   # 室内长度（米）
r_h = 3   # 室内高度（米）
V_ac = r_w * r_l * r_h  # 室内体积（立方米）
season = "summer"
# # 温度参数
if season == "summer":
    T_outdoor = 35   # 室外初始温度（摄氏度），假设为
    T_target = 24    # 室内目标温度（摄氏度）
    T_ac_out = 24    # 空调出风口温度（摄氏度）
if season == "winter":
    T_outdoor = 5   # 室外初始温度（摄氏度），假设为冬天
    T_target = 24    # 室内目标温度（摄氏度）
    T_ac_out = 24    # 空调出风口温度（摄氏度）

# 空调位置
ac_position = (2.5, 4, 1.5)

# 空调参数
ac_velocity = 8            # 空调最大风速（米/秒）
ac_flow_rate = 600         # 空调最大风量（立方米/小时）
ac_power = 1800            # 空调额定功率（瓦特）
thermal_diffusivity = 0.0000213  # 空气热扩散系数（平方米/小时）

# 网格划分参数
nx, ny, nz = 40, 40, 20  # 网格点数 (x, y, z)
x = np.linspace(0, r_w, nx)  # x 方向的网格点
y = np.linspace(0, r_l, ny)  # y 方向的网格点
z = np.linspace(0, r_h, nz)  # z 方向的网格点
X, Y, Z = np.meshgrid(x, y, z)    # 创建三维网格

# 初始化温度场，设置为室外温度
T = np.full((nx, ny, nz), T_outdoor, dtype=float)

# 空调影响区域函数
def ac_influence(x, y, z, ac_pos, radius=1):
    dist = np.sqrt((x - ac_pos[0]) ** 2 + (y - ac_pos[1]) ** 2 + (z - ac_pos[2]) ** 2)
    return np.exp(-dist ** 2 / (2 * radius ** 2))

# 设置模拟参数
# 总模拟时间为 timesteps * dt
timesteps, dt = 6000, 0.1  # 时间步数, 时间步长
times = timesteps * dt
print(f"当前运行时间是{times}s")

# 开始迭代模拟
for t in range(timesteps):

    influence = ac_influence(X, Y, Z, ac_position)  # 获取空调的影响值
    T += influence * (T_ac_out - T) * dt  # 更新温度场

    # 使用拉普拉斯算子计算空间方向上的温度变化
    # x 方向的变化
    laplacian_x = (np.roll(T, 1, axis=0) + np.roll(T, -1, axis=0) - 2 * T) / (x[1] - x[0]) ** 2
    # y 方向的变化
    laplacian_y = (np.roll(T, 1, axis=1) + np.roll(T, -1, axis=1) - 2 * T) / (y[1] - y[0]) ** 2
    # z 方向的变化
    laplacian_z = (np.roll(T, 1, axis=2) + np.roll(T, -1, axis=2) - 2 * T) / (z[1] - z[0]) ** 2
    # 合成总的拉普拉斯项
    laplacian = laplacian_x + laplacian_y + laplacian_z
    # 根据热扩散系数更新温度场
    T += thermal_diffusivity * laplacian * dt
    # 设置边界条件（墙体为绝热边界）
    T[0, :, :] = T[-1, :, :] = T[:, 0, :] = T[:, -1, :] = T[:, :, 0] = T[:, :, -1] = T_outdoor


# 可视化结果
# fig = plt.figure(figsize=(12, 6))  # 创建图形窗口
fig = plt.figure()

# 横截面温度分布 - 可视化
# ax1 = fig.add_subplot(121)  # 创建1行2列的第一个子图
# fig1 = plt.figure()
# ax1 = fig1.add_subplot()  # 绘制单张图像
# cross_section = T[:, :, r_h // 2]  # 中间高度的横截面
# im = ax1.contourf(x, y, cross_section, levels=50, cmap='coolwarm')  # 绘制等高线图
# plt.colorbar(im, ax=ax1)  # 添加颜色条
# ax1.set_title(f'Temperature distribution (middle cross-section, t={times}s)')
# ax1.set_xlabel('Width/m')
# ax1.set_ylabel('Length/m')
# fig1.tight_layout()
# plt.savefig(f"../figures/q1_{times}s_diff_{season}.png")

# 空调影响可视化
# ax2 = fig.add_subplot(122, projection='3d')
fig2 = plt.figure()
ax2 = fig2.add_subplot(projection='3d')
ac_influence_plot = ac_influence(X, Y, Z, ac_position)  # 获取空调影响
ax2.scatter(X, Y, Z, c=ac_influence_plot, cmap='coolwarm_r', alpha=0.5, s=1)  # 绘制3D散点图
ax2.set_title('Air conditioning affects the weight distribution')
ax2.set_xlabel('Width/m')
ax2.set_ylabel('Length/m')
ax2.set_zlabel('Height/m')
# 调整子图间距并显示
fig2.tight_layout()

# fig2.savefig(f"../figures/q1_{times}s_scatter_{season}.png")
# plt.show()
