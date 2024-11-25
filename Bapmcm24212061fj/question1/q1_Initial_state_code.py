import numpy as np
import matplotlib.pyplot as plt

# 房间尺寸
r_w = 5   # 室内宽度（米）
r_l = 8   # 室内长度（米）
r_h = 3   # 室内高度（米）
V_ac = r_w * r_l * r_h  # 室内体积（立方米）

# 夏天温度参数
# T_outdoor = 35   # 室外初始温度（摄氏度）
# T_target = 24    # 室内目标温度（摄氏度）
# T_ac_out = 24    # 空调出风口温度（摄氏度）
# 冬天温度参数
T_outdoor = 5   # 室外初始温度（摄氏度）
T_target = 24    # 室内目标温度（摄氏度）
T_ac_out = 24    # 空调出风口温度（摄氏度）

# 网格划分参数
nx, ny, nz = 50, 80, 30  # 网格点数 (x, y, z)
x = np.linspace(0, r_w, nx)  # x 方向的网格点
y = np.linspace(0, r_l, nx)  # y 方向的网格点
z = np.linspace(0, r_h, nx)  # z 方向的网格点
X, Y, Z = np.meshgrid(x, y, z)    # 创建三维网格

# 初始化温度场，设置为室外温度
T = np.full((nx, nx, nx), T_outdoor, dtype=float)

# 设置 (x=0, y=0) 整个 z 轴的温度为 20°C
x_index = 25  # x=0 对应的索引
y_index = 25  # y=0 对应的索引
T[x_index, y_index, :] = T_ac_out


# 创建横截面和三维散点热力图
fig = plt.figure(figsize=(16, 6))
# 绘制初始温度的散点热力图
ax1 = fig.add_subplot(121, projection='3d')
slice_density = 5
X_slice = X[::slice_density, ::slice_density, ::slice_density]
Y_slice = Y[::slice_density, ::slice_density, ::slice_density]
Z_slice = Z[::slice_density, ::slice_density, ::slice_density]
T_slice = T[::slice_density, ::slice_density, ::slice_density]
sc = ax1.scatter(X_slice, Y_slice, Z_slice, c=T_slice.flatten(), cmap="coolwarm", marker='o')
cb = plt.colorbar(sc, ax=ax1, shrink=0.5, aspect=10)
cb.set_label("Heat bars/°C", fontsize=12)  # 调整颜色条字体大小
ax1.set_title("Three-dimensional scatter temperature field distribution (t=0 s)", fontsize=14)  # 标题字体大小
ax1.set_xlabel("X/m", fontsize=10)  # X轴标签字体大小
ax1.set_ylabel("Y/m", fontsize=10)  # Y轴标签字体大小
ax1.set_zlabel("Z/m", fontsize=10)  # Z轴标签字体大小
# 绘制初始状态下中等高度的横截面热力图
ax2 = fig.add_subplot(122)
z_target = r_h / 2
z_index = np.argmin(np.abs(z - z_target))
T_slice_plane = T[:, :, z_index]
contour = ax2.contourf(x, y, T_slice_plane.T, cmap="coolwarm", levels=50)
cb2 = plt.colorbar(contour, ax=ax2)
cb2.set_label("Heat bars/°C", fontsize=12)  # 调整颜色条字体大小
ax2.set_title(f"Cross-sectional temperature distribution (z=1.2 m, t=0 s)", fontsize=14)  # 标题字体大小
ax2.set_xlabel("X/m", fontsize=10)  # X轴标签字体大小
ax2.set_ylabel("Y/m", fontsize=10)  # Y轴标签字体大小
# 调整刻度标签的字体大小
ax1.tick_params(axis='both', which='major', labelsize=10)
ax2.tick_params(axis='both', which='major', labelsize=10)
# 保存图片
# fig.savefig('../figures/q1_Initial_state_winter.png')
# fig.savefig('../figures/q1_Initial_state_summer.png')
# 显示图形
plt.tight_layout()
plt.show()