import matplotlib.pyplot as plt
import re
import numpy as np

# Read data from text file
with open('2024-09-03_10-12-44_mass.txt', 'r') as file:
    data = file.readlines()

# Initialize lists for timestamps and mass values
timestamps = []
mass_values = []

# Regular expression pattern to match the relevant parts of each line
pattern = re.compile(r'{T:(\d+),L:I,M:EXT,MASS{1:(\d+\.\d+)}')

# Extract data using regex
for line in data:
    match = pattern.search(line)
    if match:
        timestamps.append(int(match.group(1)))
        mass_values.append(float(match.group(2)))

# Calculate the derivative of the mass with respect to the timestamp
timestamps = np.array(timestamps)
mass_values = np.array(mass_values)
dmass_dt = np.gradient(mass_values, timestamps)
dmass_dt = dmass_dt*600

# Plotting the original MASS data
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(timestamps, mass_values, marker='o', linestyle='-', color='b')
plt.title('MASS vs Timestamp')
plt.xlabel('Timestamp (T)')
plt.ylabel('MASS')
plt.grid(True)

# Plotting the derivative of MASS data
plt.subplot(2, 1, 2)
plt.plot(timestamps, dmass_dt, marker='o', linestyle='-', color='r')
plt.title('Derivative of MASS vs Timestamp')
plt.xlabel('Timestamp (T)')
plt.ylabel('d(MASS)/dT')
plt.grid(True)

plt.tight_layout()
plt.show()


