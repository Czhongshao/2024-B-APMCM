# 湿度扩散系数计算
def humidity_diffusion_coefficient(T):
    # 基于温度计算扩散系数
    D0 = 2.4e-5  # 参考扩散系数 (m²/s) at 25°C
    T0 = 298.15  # 参考温度 (K) (25°C)
    T_kelvin = T + 273.15  # 转换为开尔文
    return D0 * (T_kelvin / T0) ** 1.75

# 使用示例：室温 25°C
current_temp = 25  # 当前温度 (°C)
diffusion_coeff = humidity_diffusion_coefficient(current_temp)
print(f"湿度扩散系数 (D) 在 {current_temp}°C 时为: {diffusion_coeff:.2e} m²/s")
