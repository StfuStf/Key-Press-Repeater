import time
import threading
import os
from pynput.keyboard import Controller, Key
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from Xlib import X, display  # For window management

# Initialize the keyboard controller
keyboard = Controller()

# Global variables
is_running = False
target_window_name = ""
keys_to_press = [Key.f6, Key.f7]
interval = 300  # Default interval: 5 minutes

# Configuration file path
CONFIG_FILE = "config.txt"

# Default window size
DEFAULT_WIDTH = 400
DEFAULT_HEIGHT = 200

# Function to load settings from the configuration file
def load_settings():
    global target_window_name, keys_to_press, interval
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                target_window_name = lines[0].strip()
                keys_to_press = [getattr(Key, key.strip().lower()) for key in lines[1].strip().split(",")]
                interval = int(lines[2].strip())
            if len(lines) >= 5:
                return int(lines[3].strip()), int(lines[4].strip())
    return DEFAULT_WIDTH, DEFAULT_HEIGHT

# Function to save settings to the configuration file
def save_settings():
    with open(CONFIG_FILE, "w") as file:
        file.write(f"{target_window_name}\n")
        file.write(f"{','.join([key.name for key in keys_to_press])}\n")
        file.write(f"{interval}\n")
        file.write(f"{root.winfo_width()}\n")
        file.write(f"{root.winfo_height()}\n")

# Function to simulate key presses
def press_keys():
    for key in keys_to_press:
        keyboard.press(key)
        keyboard.release(key)
        print(f"Pressed {key}")
        time.sleep(0.5)  # Short delay between key presses

# Function to check if the target window is active
def is_target_window_active():
    if not target_window_name:
        return True  # If no window is selected, always return True
    try:
        d = display.Display()
        root = d.screen().root
        # Get the active window ID
        window_id_prop = root.get_full_property(d.intern_atom("_NET_ACTIVE_WINDOW"), X.AnyPropertyType)
        if window_id_prop is None:
            return False  # No active window
        window_id = window_id_prop.value[0]
        # Get the window name
        window = d.create_resource_object("window", window_id)
        window_name_prop = window.get_full_property(d.intern_atom("_NET_WM_NAME"), X.AnyPropertyType)
        if window_name_prop is None:
            return False  # No window name
        window_name = window_name_prop.value.decode()
        return target_window_name in window_name
    except Exception as e:
        print(f"Error checking active window: {e}")
        return False

# Function to get all open windows
def get_open_windows():
    try:
        d = display.Display()
        root = d.screen().root
        # Get the list of window IDs
        window_ids_prop = root.get_full_property(d.intern_atom("_NET_CLIENT_LIST"), X.AnyPropertyType)
        if window_ids_prop is None:
            return []  # No open windows
        window_ids = window_ids_prop.value
        windows = []
        for window_id in window_ids:
            window = d.create_resource_object("window", window_id)
            try:
                # Get the window name
                window_name_prop = window.get_full_property(d.intern_atom("_NET_WM_NAME"), X.AnyPropertyType)
                if window_name_prop is not None:
                    window_name = window_name_prop.value.decode()
                    windows.append(window_name)
            except:
                pass
        return windows
    except Exception as e:
        print(f"Error getting open windows: {e}")
        return []

# Main loop
def loop():
    global is_running
    countdown = interval  # Initialize the countdown
    while is_running:
        if is_target_window_active():
            press_keys()
            while countdown > 0 and is_running:
                if not is_target_window_active():
                    countdown_label.config(text="Paused: Target window not active")
                    break  # Pause the countdown
                countdown_label.config(text=f"Next press in: {countdown} seconds")
                time.sleep(1)
                countdown -= 1
            if countdown <= 0:
                countdown = interval  # Reset the countdown
        else:
            countdown_label.config(text="Paused: Target window not active")
            time.sleep(1)

# Start the loop
def start_loop():
    global is_running
    if not is_running:
        is_running = True
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        threading.Thread(target=loop, daemon=True).start()

# Stop the loop
def stop_loop():
    global is_running
    is_running = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    countdown_label.config(text="Stopped")

# Set keys to press
def set_keys():
    global keys_to_press
    keys_input = simpledialog.askstring("Set Keys", "Enter keys to press (comma-separated, e.g., F6,F7):")
    if keys_input:
        keys_to_press = [getattr(Key, key.strip().lower()) for key in keys_input.split(",")]
        messagebox.showinfo("Keys Updated", f"Keys set to: {keys_to_press}")
        save_settings()

# Set time interval
def set_interval():
    global interval
    interval_input = simpledialog.askinteger("Set Interval", "Enter time interval in seconds:")
    if interval_input:
        interval = interval_input
        messagebox.showinfo("Interval Updated", f"Interval set to: {interval} seconds")
        save_settings()

# Set target window
def set_target_window():
    global target_window_name
    windows = get_open_windows()
    if not windows:
        messagebox.showwarning("No Windows", "No open windows detected.")
        return

    # Create a new window for selecting the target window
    select_window = tk.Toplevel(root)
    select_window.title("Select Target Window")
    select_window.geometry("300x200")

    # Dropdown menu for window selection
    tk.Label(select_window, text="Select a window:").pack(pady=10)
    window_var = tk.StringVar(value=windows[0])
    window_dropdown = ttk.Combobox(select_window, textvariable=window_var, values=windows)
    window_dropdown.pack(pady=10)

    # Confirm button
    def confirm_selection():
        global target_window_name
        target_window_name = window_var.get()
        messagebox.showinfo("Target Window Updated", f"Target window set to: {target_window_name}")
        save_settings()
        select_window.destroy()

    tk.Button(select_window, text="Confirm", command=confirm_selection).pack(pady=10)

# Handle window closing
def on_closing():
    save_settings()
    if is_running:
        messagebox.showwarning("Warning", "Please stop the script before closing.")
    else:
        root.destroy()

# Load settings when the script starts
window_width, window_height = load_settings()

# Create the GUI
root = tk.Tk()
root.title("Key Press Repeater")
root.geometry(f"{window_width}x{window_height}")

# Start Button
start_button = tk.Button(root, text="Start", command=start_loop, font=("Arial", 14))
start_button.pack(pady=10)

# Stop Button
stop_button = tk.Button(root, text="Stop", command=stop_loop, state=tk.DISABLED, font=("Arial", 14))
stop_button.pack(pady=10)

# Set Keys Button
set_keys_button = tk.Button(root, text="Set Keys", command=set_keys, font=("Arial", 12))
set_keys_button.pack(pady=5)

# Set Interval Button
set_interval_button = tk.Button(root, text="Set Interval", command=set_interval, font=("Arial", 12))
set_interval_button.pack(pady=5)

# Set Target Window Button
set_window_button = tk.Button(root, text="Set Target Window", command=set_target_window, font=("Arial", 12))
set_window_button.pack(pady=5)

# Countdown Label
countdown_label = tk.Label(root, text="Stopped", font=("Arial", 14))
countdown_label.pack(pady=10)

# Handle window closing
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI
root.mainloop()
