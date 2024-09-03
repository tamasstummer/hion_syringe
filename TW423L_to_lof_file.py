import serial
import os
desktop = os.path.expanduser("~/Desktop")

from datetime import datetime

def read_from_serial_and_write_to_file(serial_port, baud_rate, output_file):
    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    
    start_time = datetime.now()

    with open(output_file, 'w') as file:
        buffer = ''
        while True:
            if ser.in_waiting > 0:
                # Read a single character from the serial port
                char = ser.read().decode('utf-8')
                buffer += char
                # If the character is a Carriage Return, process the buffer
                if char == '\r':
                    # Calculate elapsed time in milliseconds
                    elapsed_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
                    # Remove the Carriage Return from the end
                    line = buffer[:-1]
                    try:
                        strValue = line.replace(' ','').replace('g', '')
                        # Convert the line to a float
                        number = float(strValue)
                        #number = int(number*1000)
                        # Format the line with elapsed time in milliseconds
                        #formatted_line = f"{elapsed_time_ms} {number}"
                        formatted_line = "{T:"+str(elapsed_time_ms)+",L:I,M:EXT,MASS{1:"+str(number)+"}"
                        # Write the formatted line to the file
                        file.write(formatted_line + '\n')
                        # Optionally, print to the console for debugging
                        print(formatted_line)
                    except ValueError:
                        # If the line is not a valid float, skip it
                        #print(f"Invalid input: {line}")
                        eventStr = "{T:"+str(elapsed_time_ms)+",L:I,M:EXT,E:"+line+"}"
                        file.write(eventStr + '\n')
                        print(eventStr)
                    # Clear the buffer
                    buffer = ''

# Replace 'COM7' with your serial port and set the correct baud rate
serial_port = 'COM7'
baud_rate = 1200

# Create the output file name with the current date and time
desktopFolder = os.path.normpath(os.path.expanduser("~/Desktop/Syringe"))
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
output_file = f'{desktopFolder}/{current_time}_mass.txt'
print("Output file located at: "+output_file)

read_from_serial_and_write_to_file(serial_port, baud_rate, output_file)