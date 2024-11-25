import numpy as np
import matplotlib.pyplot as plt

# 房间和净化器参数
r_w, r_l, r_h = 5, 8, 3  # 房间尺寸（米）
ROOM_VOLUME = r_w * r_l * r_h  # 房间体积（立方米）
D_DIFF = 5e-4  # 扩散系数（平方米/秒）
PM_INIT = 100  # 初始污染物浓度（微克/立方米）
T_SIM, DT = 6000, 0.1  # 总步数，步长
times = T_SIM * DT
print(f"当前运行时间:{times}s")
NX, NY, NZ = 40, 40, 20  # 网格点数 (x, y, z)

# 净化器设计参数
D_best = 0.27  # 直径 (m)
H_best = 1.60  # 高度 (m)
N_filter = 8  # 滤网层数
N_in = 3  # 进风口数量
N_out = 3  # 出风口数量
CADR_best = 576.00  # 最佳 CADR (m³/h)
radius = 1  # 净化器影响半径

# 净化器高斯影响函数
def purifier_influence(X, Y, Z, pos, radius):
    dist = np.sqrt((X - pos[0])**2 + (Y - pos[1])**2 + (Z - pos[2])**2)
    return np.exp(-dist**2 / (2 * radius**2))

# 初始化污染物浓度和净化器影响
dx, dy, dz = r_w / (NX - 1), r_l / (NY - 1), r_h / (NZ - 1)
x, y, z = np.linspace(0, r_w, NX), np.linspace(0, r_l, NY), np.linspace(0, r_h, NZ)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

C = np.ones((NX, NY, NZ)) * PM_INIT  # 初始污染物浓度
pur_position = (r_w / 2, r_l / 2, H_best / 2)  # 净化器位置
I = purifier_influence(X, Y, Z, pur_position, radius=radius)

# 扩散和净化模拟
K_FILTER = 0.8  # 过滤器效率常数
for t in range(T_SIM):
    laplacian = (
        (np.roll(C, 1, axis=0) - 2 * C + np.roll(C, -1, axis=0)) / dx**2 +
        (np.roll(C, 1, axis=1) - 2 * C + np.roll(C, -1, axis=1)) / dy**2 +
        (np.roll(C, 1, axis=2) - 2 * C + np.roll(C, -1, axis=2)) / dz**2
    )
    # 更新污染物浓度
    C_new = C + D_DIFF * laplacian * DT
    C_new *= (1 - K_FILTER * I * DT)  # 净化器影响
    C_new = np.clip(C_new, 0, PM_INIT)  # 限制浓度范围

    # 设置边界条件
    C_new[0, :, :] = C_new[-1, :, :] = C_new[:, 0, :] = C_new[:, -1, :] = C_new[:, :, 0] = C_new[:, :, -1] = PM_INIT
    C = C_new

# 可视化污染物浓度分布
# 横截面（z=中间高度）
fig1, ax1 = plt.subplots(figsize=(8, 6))
cross_section = C[:, :, NZ // 2]  # 中间高度的横截面
im = ax1.contourf(x, y, cross_section.T, levels=50, cmap='coolwarm')
plt.colorbar(im, ax=ax1, label="PM2.5 Concentration (µg/m³)")
ax1.set_title(f'PM2.5 Concentration (Cross-Section, t={times}s)')
ax1.set_xlabel("Width/m")
ax1.set_ylabel("Length/m")
plt.tight_layout()
plt.savefig(f'../figures/q2_PM2.5_cross_section_{times}s.png')

# 三维散点图
fig2 = plt.figure()
ax2 = fig2.add_subplot(projection='3d')
sc = ax2.scatter(
    X.ravel(), Y.ravel(), Z.ravel(),
    c=C.ravel(), cmap="coolwarm", s=1.5, alpha=0.5
)
ax2.set_title("PM2.5 Distribution (3D View)")
ax2.set_xlabel("Width/m")
ax2.set_ylabel("Length/m")
ax2.set_zlabel("Height/m")
cbar = plt.colorbar(sc, ax=ax2, shrink=0.5, pad=0.1)
cbar.set_label("PM2.5 Concentration (µg/m³)")
plt.tight_layout()
plt.savefig(f'../figures/q2_PM2.5_3D_{times}s.png')

plt.show()

fig1 = plt.figure()
# 添加第一个子图（等高线图），位于第一行
# ax1 = fig.add_subplot(211)
ax1 = fig1.add_subplot()
cs = ax1.contourf(x, y, C[:, :, NZ // 2].T, levels=20, cmap='BuGn_r', vmin=0, vmax=PM_INIT)
fig1.colorbar(cs, ax=ax1, label='Concentration (µg/m³)')
ax1.set_title('PM2.5 Concentration (Mid Height)')
ax1.set_xlabel('Width/m')
ax1.set_ylabel('Length/m')
plt.tight_layout()
# plt.savefig(f'../figures/q2_PM2.5_diff_{times}s.png')


# 添加第二个子图（3D散点图），位于第二行
# ax2 = fig.add_subplot(212, projection='3d')
fig2 = plt.figure()
ax2 = fig2.add_subplot(projection='3d')
sc = ax2.scatter(
    X.ravel(), Y.ravel(), Z.ravel(),
    c=I.ravel(),  # 使用污染值决定颜色
    cmap="BuGn",  # 可以选择其他颜色映射，如 'coolwarm', 'viridis' 等
    s=1.5, alpha=0.8  # 调整点的大小和透明度
)

ax2.set_title("Purifier Influence Distribution")
ax2.set_xlabel("Width/m")
ax2.set_ylabel("Length/m")
ax2.set_zlabel("Height/m")
plt.tight_layout()
# plt.savefig(f'../figures/q2_PM2.5_concentration_{times}s.png')
# plt.savefig(f'../figures/q2_PM2.5_3-scatter_{times}s.png')
# plt.show()