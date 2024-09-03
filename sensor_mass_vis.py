import matplotlib.pyplot as plt
import re
import numpy as np
import os
from datetime import datetime

# Define the file name or leave it empty to select the latest automatically
filename = ''

# If filename is empty, find the latest file
if not filename:
    # List all .txt files in the current directory
    txt_files = [f for f in os.listdir() if f.endswith('.txt')]
    
    # Filter files that match the naming pattern (datetime_mass)
    valid_files = [f for f in txt_files if re.match(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_mass\.txt', f)]
    
    # Sort the files by datetime in the name and get the latest one
    latest_file = max(valid_files, key=lambda x: datetime.strptime(x.split('_')[0] + '_' + x.split('_')[1], '%Y-%m-%d_%H-%M-%S'))
    
    filename = latest_file

# Read data from the selected text file
with open(filename, 'r') as file:
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


