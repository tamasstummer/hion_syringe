import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import threading

class STM32Controller(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("STM32 Controller")
        self.geometry("800x600")

        self.serial_port = None

        self.create_widgets()
        self.update_ports()
        self.schedule_port_update()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # COM port selection frame
        com_frame = tk.Frame(main_frame)
        com_frame.pack(fill=tk.X, pady=10)

        self.com_label = tk.Label(com_frame, text="Select COM Port:")
        self.com_label.pack(side=tk.LEFT)

        self.com_combobox = ttk.Combobox(com_frame)
        self.com_combobox.pack(side=tk.LEFT, padx=5)

        self.connect_button = tk.Button(com_frame, text="Connect", command=self.connect_com_port)
        self.connect_button.pack(side=tk.LEFT, padx=5)

        self.disconnect_button = tk.Button(com_frame, text="Disconnect", state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, padx=5)

        # Control buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)

        self.operate_button = tk.Button(buttons_frame, text="OPERATE", state=tk.DISABLED)
        self.operate_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = tk.Button(buttons_frame, text="PAUSE", command=lambda: self.send_command("P"), state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(buttons_frame, text="RESET", state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Parameters settings frame
        params_frame = tk.Frame(main_frame)
        params_frame.pack(fill=tk.X, pady=10)

        self.create_parameter_input(params_frame, "Valve Change Time (ms):", "A", 100)
        self.create_parameter_input(params_frame, "Motor Push Velocity (%):", "B", 80)
        self.create_parameter_input(params_frame, "Motor Buildup Pressure Velocity (%):", "C", 10)
        self.create_parameter_input(params_frame, "Motor Pull Velocity (%):", "D", 100)
        self.create_parameter_input(params_frame, "Pressure Offset:", "E", 5)
        self.create_parameter_input(params_frame, "Syringe Full State Fill Time (ms):", "F", 2000)  # New parameter

        # Message log frame
        log_frame = tk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.log_label = tk.Label(log_frame, text="Log Messages:")
        self.log_label.pack(anchor=tk.W)

        self.clear_log_button = tk.Button(log_frame, text="Clear Log", command=self.clear_log)
        self.clear_log_button.pack(anchor=tk.E)

        self.log_textbox = tk.Text(log_frame, state=tk.DISABLED)
        self.log_textbox.pack(fill=tk.BOTH, expand=True)

    def create_parameter_input(self, parent, label_text, short_name, default_value):
        frame = tk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame)
        entry.insert(0, str(default_value))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        send_button = tk.Button(frame, text="Send", command=lambda: self.send_single_parameter(short_name, entry.get()))
        send_button.pack(side=tk.LEFT, padx=5)

    def update_ports(self):
        ports = serial.tools.list_ports.comports()
        self.com_combobox['values'] = [port.device for port in ports]

    def schedule_port_update(self):
        self.update_ports()
        self.after(5000, self.schedule_port_update)  # Update every 5 seconds

    def connect_com_port(self):
        port = self.com_combobox.get()
        if port:
            try:
                self.serial_port = serial.Serial(port, 9600, timeout=1)
                self.connect_button.config(text="Connected", state="disabled", bg="green")
                self.log_message(f"Connected to {port} at 9600 baud rate", "green")
            except serial.SerialException as e:
                self.log_message(f"Failed to connect to {port}: {e}", "red")

    def send_command(self, command):
        if self.serial_port and self.serial_port.is_open:
            full_command = command.ljust(15, 'x')
            self.serial_port.write(full_command.encode())
            self.log_message(f"Sent: {full_command}", "blue")
        else:
            self.log_message("COM port is not connected", "red")

    def send_single_parameter(self, short_name, param_value):
        full_command = f"{short_name}{param_value}".ljust(15, 'x')
        self.send_command(full_command)

    def log_message(self, message, color="black"):
        self.log_textbox.config(state=tk.NORMAL)
        self.log_textbox.insert(tk.END, message + '\n', color)
        self.log_textbox.tag_config(color, foreground=color)
        self.log_textbox.config(state=tk.DISABLED)
        self.log_textbox.yview(tk.END)

    def clear_log(self):
        self.log_textbox.config(state=tk.NORMAL)
        self.log_textbox.delete(1.0, tk.END)
        self.log_textbox.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = STM32Controller()
    app.mainloop()
