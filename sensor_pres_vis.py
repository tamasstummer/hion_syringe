import matplotlib.pyplot as plt
import re
import numpy as np

# Read data from text file
with open('2024-08-29_14-48-31_syringe.txt', 'r') as file:
    data = file.readlines()

# Initialize lists for timestamps and pressure values
timestamps = []
pres1_values = []
pres2_values = []

# Regular expression pattern to match the relevant parts of each line
pattern = re.compile(r'{T:(\d+),L:I,M:ANL,PRES:{1:(\d+\.\d+),2:(\d+\.\d+)}}')

# Extract data using regex
for line in data:
    match = pattern.search(line)
    if match:
        timestamps.append(int(match.group(1)))
        pres1_values.append(float(match.group(2)))
        pres2_values.append(float(match.group(3)))

# Convert lists to numpy arrays for further processing
timestamps = np.array(timestamps)
pres1_values = np.array(pres1_values)
pres2_values = np.array(pres2_values)

# Plotting both PRES1 and PRES2 in the same graph
plt.figure(figsize=(12, 6))
plt.plot(timestamps, pres1_values, marker='o', linestyle='-', color='b', label='PRES1')
plt.plot(timestamps, pres2_values, marker='o', linestyle='-', color='r', label='PRES2')

plt.title('PRESSURE 1 and PRESSURE 2 vs Timestamp')
plt.xlabel('Timestamp (T)')
plt.ylabel('PRESSURE')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
