import numpy as np
import matplotlib.pyplot as plt

# 房间参数（单位：米）
r_w, r_l, r_h = 5, 8, 3  # 房间尺寸（宽，长，高）

# 空气属性
rho = 1.2  # 空气密度（kg/m^3）
c_p = 1005  # 比热容（J/(kg·K)）

# 空调风量参数
V_dot_in = 0.03 * 3.0  # 进风量（m^3/s）
V_dot_out = 0.05 * 5.0  # 出风量（m^3/s）

# 温度参数（单位：摄氏度）
season = "winter"
# # 温度参数
if season == "summer":
    T_outdoor = 35   # 室外初始温度（摄氏度），假设为
    T_target = 24    # 室内目标温度（摄氏度）
    T_ac_out = 20    # 空调出风口温度（摄氏度）
if season == "winter":
    T_outdoor = 5   # 室外初始温度（摄氏度），假设为冬天
    T_target = 24    # 室内目标温度（摄氏度）
    T_ac_out = 28    # 空调出风口温度（摄氏度）

# 热扩散率（m^2/s）
thermal_diffusivity = 0.0000215

# 初始化网格和温度场
nx, ny, nz = 50, 80, 30  # 网格大小（x, y, z）
T = np.full((nx, ny, nz), T_outdoor, dtype=float)  # 初始温度场

# 计算空气质量（kg）
m_air = rho * r_w * r_l * r_h  # 房间空气质量（kg）

# 风量（kg/s）
m_dot_ac = rho * (V_dot_in + V_dot_out) / 2  # 平均风量

# 时间参数
t_total, dt = 3600, 1  # 总时间和时间步长
time = np.arange(0, t_total + dt, dt)  # 时间数组

# 初始化室内温度数组
T_room = np.zeros(len(time))
T_room[0] = T_outdoor  # 初始温度

# 温度方程系数
alpha = m_dot_ac / m_air  # 质量流速系数（1/s）
beta = 1 / (m_air * c_p)  # 热传递系数（1/s）

# 模拟循环
for i in range(1, len(time)):
    T_current = T_room[i - 1]
    # 能量平衡方程
    dTdt = - alpha * (T_current - T_ac_out) - beta * (T_current - T_outdoor)
    T_next = T_current + dTdt * dt
    # 更新温度
    T_room[i] = T_next
    # 检查是否达到目标温度
    if season == 'winter':
        if T_next >= T_target: # 冬季
            print(f"At {time[i]} seconds, the indoor temperature reaches the target of {T_target}°C.")
            T_room = T_room[:i+1]
            time = time[:i+1]
            times = time[i]
            break
    if season == 'summer':
        if T_next <= T_target: # 夏季
            print(f"At {time[i]} seconds, the indoor temperature reaches the target of {T_target}°C.")
            T_room = T_room[:i+1]
            time = time[:i+1]
            times = time[i]
            break

# 绘制温度随时间变化的图表
plt.plot(time, T_room)
plt.xlabel('Time/s')
plt.ylabel('AVG Temperature/°C')
plt.title(f"{season} enviroment(Target Temperature={T_target}°C time={times}s)")
plt.grid(True)
plt.tight_layout()
# plt.savefig(f"../figures/q1_avg_temperature_{season}.png")
plt.show()