"""
此段代码用于第一问计算出口风的雷诺数
结果如下:
当前的出口长度: 0.60米, 宽度: 0.30米
在速度V=1m/s时, 雷诺数Re=26666.67
在速度V=2m/s时, 雷诺数Re=53333.33
在速度V=3m/s时, 雷诺数Re=80000.0
在速度V=4m/s时, 雷诺数Re=106666.67
在速度V=5m/s时, 雷诺数Re=133333.33
在速度V=6m/s时, 雷诺数Re=160000.0
在速度V=7m/s时, 雷诺数Re=186666.67
在速度V=8m/s时, 雷诺数Re=213333.33
"""
# 空调参数
out_length = 0.6 # 出口大小(米)
out_width = 0.3
ac_velocity = 8  # 空调最大风速（米/秒）

# 空气参数
miu_air = 1.8 * 10 ** -5  # 空气动力粘度
rou_air = 1.2  # 空气密度
D_air = (4 * out_width * out_length) / (2 * (out_length + out_width))  # 特征长度
print(f"当前的出口长度: {out_length:.2f}米, 宽度: {out_width:.2f}米")
# 计算雷诺数并保留两位小数
for i in range(1, ac_velocity + 1, 1):
    Re = (rou_air * D_air * i) / miu_air
    print(f"在速度V={i}m/s时, 雷诺数Re={round(Re, 2)}")

