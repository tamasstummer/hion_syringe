import serial
import os
import re
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def receive_and_save_data(port, baudrate):
    try:
        # Create the output directory if it doesn't exist
        desktop_folder = os.path.normpath(os.path.expanduser("~/Desktop/Syringe"))
        os.makedirs(desktop_folder, exist_ok=True)
        logging.info(f"Output directory is set to: {desktop_folder}")

        # Create the output file name with the current date and time
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = f'{desktop_folder}/{current_time}_syringe.txt'
        logging.info(f"Output file located at: {output_file}")

        # Open the serial port and output file
        ser = serial.Serial(port, baudrate, timeout=1)
        file = open(output_file, 'w')

        logging.info(f"Connected to {port} at {baudrate} baud.")

        start_time = datetime.now()

        while True:
            # Read data from the serial port
            data = ser.readline()
            if data:
                # Decode data from bytes to string
                line = data.decode('utf-8').strip()
                logging.debug(f"Received: {line}")

                # Check if the line is a JSON-like message
                if 0:#line.startswith('{') and line.endswith('}'):
                    # Calculate elapsed time in milliseconds
                    elapsed_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
                    # Replace the existing timestamp with the new timestamp
                    modified_line = re.sub(r'T:\d+', f'T:{elapsed_time_ms}', line)
                    logging.debug(f"Modified line: {modified_line}")
                    # Save modified data to the file
                    file.write(modified_line + '\n')
                else:
                    # Save unmodified data to the file
                    file.write(line + '\n')

                # Ensure data is written to the file
                file.flush()
                os.fsync(file.fileno())

    except serial.SerialException as e:
        logging.error(f"Serial exception: {e}")
    except KeyboardInterrupt:
        logging.info("Exiting program.")
    finally:
        if 'file' in locals():
            file.flush()
            file.close()
            logging.info("File closed properly.")
        if 'ser' in locals() and ser.is_open:
            ser.close()
            logging.info("Serial port closed properly.")

if __name__ == "__main__":
    # Modify these variables according to your setup
    COM_PORT = 'COM5'     # Replace with your COM port
    BAUD_RATE = 115200      # Replace with your baud rate

    logging.info("Starting data reception...")
    receive_and_save_data(COM_PORT, BAUD_RATE)
    logging.info("Data reception ended.")
