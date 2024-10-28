import subprocess
import time
import math


SECONDS = 50
current_values = []
voltage_values = []
power_values = []

def read_values():
    result = subprocess.run(['vcgencmd', 'pmic_read_adc'], capture_output=True, text=True)
    output = result.stdout.strip().splitlines()

    #extracting voltage and current values
    current = None
    voltage = None
    
    print(output)
    print('----')

    for line in output:
        if "current" in line:
            current = float(line.split('=')[-1].strip('A'))
        if "volt" in line:
            voltage = float(line.split('=')[-1].strip('V'))

    return current, voltage

def calculate_average_and_error(values):
    n = len(values)
    if n == 0:
        return 0,0

    sum_x = sum(values)
    sum_x2 = sum([x**2 for x in values])

    average = (sum_x / n) * 1.1451 + 0.5879
    #error = math.sqrt((sum_x2 - (sum_x**2)/n) / (n-1) - n) * 1.1451 if n > 1 else 0
    variance_term = (sum_x2 - (sum_x** 2) / n) / (n - 1) if n > 1 else 0
    if variance_term < 0:
        variance_term = 0
    
    error = math.sqrt(variance_term / n) * 1.1451 if n > 1 else 0

    return average, error



#Main script
for _ in range(SECONDS):
    time.sleep(1)
    current, voltage = read_values()
    #print(f'CURRENT: {current}')
    #print(f'VOLTAGE: {voltage}')

    if current is not None and voltage is not None:
        power = current * voltage
        power_values.append(power)

average_power, error = calculate_average_and_error(power_values)

print(f"\nAverage_power_consumption= {average_power:.3f} +/- {error:.3f} W") 

