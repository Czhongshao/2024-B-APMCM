"""
此段代码用于第一问计算标准空气热扩散系数(单位:平方米/秒)
结果如下:
标准的空气热扩散系数:2.155887230514096e-05
2.15 * 10^-5
"""
rou_air = 1.2 # 空气密度
k_air = 0.026
c_air = 1005

thermal_diffusivity = k_air / (rou_air * c_air)
print(f"标准的空气热扩散系数:{thermal_diffusivity}")
