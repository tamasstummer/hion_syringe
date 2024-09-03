import matplotlib.pyplot as plt
import re
import numpy as np

# Read data from text file
with open('2024-08-29_14-48-31_mass.txt', 'r') as file:
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

# Convert lists to numpy arrays for further processing
timestamps = np.array(timestamps)
mass_values = np.array(mass_values)

# Calculate the differences between consecutive timestamps
timestamp_diffs = np.diff(timestamps)

# Calculate the derivative of the mass with respect to the timestamp
#dmass_dt = np.diff(mass_values)
#dmass_dt = np.gradient(mass_values, timestamps)
#dmass_dt = dmass_dt * timestamp_diffs  # scaling factor

# Initialize an empty list to store the differences
dmass_dt = []

# Use a for loop to calculate the differences between consecutive elements
for i in range(1, len(mass_values)):
    difference = mass_values[i] - mass_values[i - 1]
    dmass_dt.append(difference)

# Convert the result back to a numpy array if needed
dmass_dt = np.array(dmass_dt)

print(dmass_dt[1000:1100])
print(mass_values[1000:1100])

# Plotting the original MASS data and timestamp differences in a single figure
plt.figure(figsize=(12, 8))

# First subplot: MASS vs Timestamp
plt.subplot(3, 1, 1)
plt.plot(timestamps, mass_values, marker='o', linestyle='-', color='b')
plt.title('MASS vs Timestamp')
plt.xlabel('Timestamp (T)')
plt.ylabel('MASS')
plt.grid(True)

# Second subplot: Derivative of MASS vs Timestamp
plt.subplot(3, 1, 2)
plt.plot(timestamps[1:], dmass_dt, marker='o', linestyle='-', color='r')
plt.title('Derivative of MASS vs Timestamp')
plt.xlabel('Timestamp (T)')
plt.ylabel('d(MASS)/dT')
plt.grid(True)

# Third subplot: Timestamp Differences
# For timestamp differences, we use timestamps[1:] because np.diff reduces the size of the array by 1
plt.subplot(3, 1, 3)
plt.plot(timestamps[1:], timestamp_diffs, marker='o', linestyle='-', color='g')
plt.title('Timestamp Differences')
plt.xlabel('Timestamp (T)')
plt.ylabel('ΔT (Timestamp Differences)')
plt.grid(True)

# Display the plot with a tight layout
plt.tight_layout()
plt.show()
