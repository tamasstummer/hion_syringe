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
    
    # Filter files that match the naming pattern (datetime_syringe or datetime_mass)
    valid_files = [f for f in txt_files if re.match(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_syringe\.txt', f)]
    
    # Sort the files by datetime in the name and get the latest one
    latest_file = max(valid_files, key=lambda x: datetime.strptime(x.split('_')[0] + '_' + x.split('_')[1], '%Y-%m-%d_%H-%M-%S'))
    
    filename = latest_file

# Read data from the selected text file
with open(filename, 'r') as file:
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
