import numpy as np
import skfuzzy as fuzzy
import matplotlib.pyplot as plt


temp_range = np.arange(0,41,1)
fan_speed_range = np.arange(0,11,1)

cold = fuzzy.trimf(temp_range, [0,0,20])
warm = fuzzy.trimf(temp_range, [10,20,30])
hot = fuzzy.trimf(temp_range, [20, 30, 40])


slow = fuzzy.trimf(fan_speed_range, [0,0,5])
medium = fuzzy.trimf(fan_speed_range, [0,5,10])
fast = fuzzy.trimf(fan_speed_range,[5,10,10])

# Rules 
# IF TEMP IS COLD THEN FAN SPEEN IS SLOW;
# IF TEMP IS WARM THEN FAN SPEED IS MEDIUM;
# IF TEMP IS HOT THEN FAN SPEED IS FAST;

Temp_value = float(input("What is the Temperature outside ? "))

Temp_cold_memb_val = fuzzy.interp_membership(temp_range, cold, Temp_value)
Temp_warm_memb_val = fuzzy.interp_membership(temp_range, warm, Temp_value)
Temp_hot_memb_val = fuzzy.interp_membership(temp_range, hot, Temp_value)

print(f"Membership in Cold: {Temp_cold_memb_val}")
print(f"Membership in Warm: {Temp_warm_memb_val}")
print(f"Membership in Hot: {Temp_hot_memb_val}")



# fan_speed_slow = np.fmin(slow, Temp_cold_memb_val)
# fan_speed_med = np.fmin(medium,Temp_warm_memb_val)
# fan_speed_fast = np.fmin(fast,Temp_hot_memb_val)

fan_speed_slow = np.minimum(slow, Temp_cold_memb_val)
fan_speed_med = np.minimum(medium,Temp_warm_memb_val)
fan_speed_fast = np.minimum(fast,Temp_hot_memb_val)

agragate = np.fmax(fan_speed_fast, np.fmax(fan_speed_med, fan_speed_slow))


crisp_speed = fuzzy.defuzz(fan_speed_range, agragate, 'centroid');

print(f"The crisp fan Speed is {crisp_speed}")

plt.figure(figsize=(8, 6))

# Plot Temperature fuzzy sets
plt.plot(temp_range, cold, label='Cold', color='blue')
plt.plot(temp_range, warm, label='Warm', color='green')
plt.plot(temp_range, hot, label='Hot', color='red')
plt.axvline(Temp_value, color='black', linestyle='--', label=f'Temperature = {Temp_value}°C')

# plt.axvline(Temp_value)

plt.title('Temperature Fuzzy Sets')
plt.xlabel('Temperature (°C)')
plt.ylabel('Membership')
plt.legend()
plt.show()