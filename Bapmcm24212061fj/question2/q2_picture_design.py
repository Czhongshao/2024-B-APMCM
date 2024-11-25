import numpy as np
import matplotlib.pyplot as plt

# 最佳净化器设计参数
D_best = 0.24  # 直径 (m)
H_best = 1.90  # 高度 (m)
N_in_best = 2  # 进风口数量
N_out_best = 4  # 出风口数量

# 可视化最佳设计的外形（圆柱形）
fig = plt.figure(figsize=(8, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制圆柱体
theta = np.linspace(0, 2 * np.pi, 30)  # 定义圆柱体的圆周角度
z = np.linspace(0, H_best, 30)  # 定义圆柱体的高度
theta, z = np.meshgrid(theta, z)  # 创建角度和高度的网格
x = (D_best / 2) * np.cos(theta)  # 计算圆柱体表面的x坐标
y = (D_best / 2) * np.sin(theta)  # 计算圆柱体表面的y坐标
ax.plot_surface(x, y, z, color='cyan', alpha=0.6, linewidth=0)  # 绘制半透明的圆柱体表面

# 绘制进风口和出风口（简化为圆形）
inlet_radius = D_best * 0.1  # 进风口半径
outlet_radius = D_best * 0.1  # 出风口半径

# 进风口
for i in range(N_in_best):
    angle = i * (360 / N_in_best)  # 计算每个进风口的角度
    rad = np.radians(angle)  # 将角度转换为弧度
    inlet_x = inlet_radius * np.cos(rad)  # 计算进风口的x坐标
    inlet_y = inlet_radius * np.sin(rad)  # 计算进风口的y坐标
    inlet_z = H_best / 2  # 进风口的z坐标（位于圆柱体中部）
    ax.scatter(inlet_x, inlet_y, inlet_z, color='blue', s=100, label='Inlet' if i == 0 else "")  # 绘制进风口

# 出风口
for i in range(N_out_best):
    angle = i * (360 / N_out_best)  # 计算每个出风口的角度
    rad = np.radians(angle)  # 将角度转换为弧度
    outlet_x = outlet_radius * np.cos(rad)  # 计算出风口的x坐标
    outlet_y = outlet_radius * np.sin(rad)  # 计算出风口的y坐标
    outlet_z = H_best / 2  # 出风口的z坐标（位于圆柱体中部）
    ax.scatter(outlet_x, outlet_y, outlet_z, color='red', s=100, label='Outlet' if i == 0 else "")  # 绘制出风口

ax.set_xlabel('X (m)')  # 设置x轴标签
ax.set_ylabel('Y (m)')  # 设置y轴标签
ax.set_zlabel('Z (m)')  # 设置z轴标签
ax.set_title('Optimal Air Purifier Design')  # 设置图表标题
ax.legend()  # 显示图例
plt.savefig("../figures/q2_best_design.png")
plt.show()  # 显示图表