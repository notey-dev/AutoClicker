import configparser
import os
import random
import threading
import tkinter as tk
from random import uniform
from time import sleep
from tkinter import messagebox, ttk

import keyboard
import mouse

VERSION = "0.2.0"


class AutoClickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"AutoClicker by Notey v{VERSION}")
        self.geometry("650x200")
        self.config_file = "config.ini"
        self.create_widgets()
        self.load_config()
        self.clicking = False
        self.click_count = 0
        self.click_thread = None
        self.stop_event = threading.Event()
        self.hotkey_toggle = "f11"
        self.click_type = "left"  # Default click type
        self.setup_hotkeys()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Status Label
        self.status_label = ttk.Label(self, text="Status: Stopped")
        self.status_label.place(x=10, y=10)

        # Frame for interval inputs
        self.interval_frame = ttk.Frame(self)

        # Interval Label and Entry for Minutes
        self.interval_label_min = ttk.Label(self.interval_frame, text="Interval (min):")
        self.interval_label_min.grid(row=0, column=0, padx=5)

        self.interval_entry_min = tk.Entry(
            self.interval_frame, width=10, borderwidth=2, relief="solid"
        )
        self.interval_entry_min.grid(row=0, column=1, padx=5)

        # Interval Label and Entry for Seconds
        self.interval_label_sec = ttk.Label(self.interval_frame, text="Interval (sec):")
        self.interval_label_sec.grid(row=0, column=2, padx=5)

        self.interval_entry_sec = tk.Entry(
            self.interval_frame, width=10, borderwidth=2, relief="solid"
        )
        self.interval_entry_sec.grid(row=0, column=3, padx=5)

        # Interval Label and Entry for Milliseconds
        self.interval_label_ms = ttk.Label(self.interval_frame, text="Interval (ms):")
        self.interval_label_ms.grid(row=0, column=4, padx=5)

        self.interval_entry_ms = tk.Entry(
            self.interval_frame, width=10, borderwidth=2, relief="solid"
        )
        self.interval_entry_ms.grid(row=0, column=5, padx=5)

        # Random Delay Label and Entry for Milliseconds
        self.random_delay_label_ms = ttk.Label(self, text="Random Delay (ms):")
        self.random_delay_label_ms.place(x=10, y=80)

        self.random_delay_entry_ms = tk.Entry(
            self, width=10, borderwidth=2, relief="solid"
        )
        self.random_delay_entry_ms.place(x=125, y=80)

        # Click Type Label and Dropdown
        self.click_type_label = ttk.Label(self, text="Click Type:")
        self.click_type_label.place(x=10, y=110)

        self.click_type_combo = ttk.Combobox(self, width=15, state="readonly")
        self.click_type_combo["values"] = (
            "Left",
            "Right",
            "Double Left",
            "Double Right",
        )
        self.click_type_combo.current(0)  # Set default to 'Left'
        self.click_type_combo.place(x=85, y=110)
        self.click_type_combo.bind("<<ComboboxSelected>>", self.on_click_type_changed)

        # Start Button
        self.start_button = ttk.Button(self, text="Start", command=self.start_clicking)
        self.start_button.place(x=475, y=160)

        # Stop Button
        self.stop_button = ttk.Button(self, text="Stop", command=self.stop_clicking)
        self.stop_button.place(x=550, y=160)

        # Hotkey Label and Entry
        self.hotkey_label = ttk.Label(self, text="Hotkey:")
        self.hotkey_label.place(x=10, y=150)

        self.hotkey_entry = tk.Entry(self, width=10, borderwidth=2, relief="solid")
        self.hotkey_entry.place(x=70, y=150)
        self.hotkey_entry.bind("<FocusIn>", self.capture_hotkey)

        # Center the interval frame
        self.update_idletasks()  # Update "requested size" from geometry manager
        window_width = self.winfo_width()
        frame_width = self.interval_frame.winfo_reqwidth()
        x_position = (window_width - frame_width) // 2
        self.interval_frame.place(x=x_position, y=40)

    def on_click_type_changed(self, event):
        selection = self.click_type_combo.get()
        if selection == "Left":
            self.click_type = "left"
        elif selection == "Right":
            self.click_type = "right"
        elif selection == "Double Left":
            self.click_type = "double_left"
        elif selection == "Double Right":
            self.click_type = "double_right"

    def setup_hotkeys(self):
        keyboard.add_hotkey(self.hotkey_toggle, self.toggle_clicking)

    def capture_hotkey(self, event):
        self.hotkey_entry.delete(0, tk.END)
        self.hotkey_entry.insert(0, "Press any key...")
        self.hotkey_entry.update()
        threading.Thread(target=self.wait_for_hotkey).start()

    def wait_for_hotkey(self):
        event = keyboard.read_event()
        if (
            event.event_type == keyboard.KEY_DOWN
            or event.event_type == keyboard.MOUSE_DOWN
        ):
            self.hotkey_toggle = event.name
            self.hotkey_entry.delete(0, tk.END)
            self.hotkey_entry.insert(0, self.hotkey_toggle)
            keyboard.unhook_all_hotkeys()
            self.setup_hotkeys()

    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        if not self.clicking:
            try:
                interval_min = float(self.interval_entry_min.get() or 0)
                interval_sec = float(self.interval_entry_sec.get() or 0)
                interval_ms = float(self.interval_entry_ms.get() or 0)
                random_delay_ms = float(self.random_delay_entry_ms.get() or 0)
                total_interval_ms = (
                    (interval_min * 60 * 1000) + (interval_sec * 1000) + interval_ms
                )

                if total_interval_ms <= 0:
                    raise ValueError("Interval must be greater than 0")

                self.clicking = True
                self.click_count = 0  # Reset click count
                self.update_status()
                self.stop_event.clear()
                self.click_thread = threading.Thread(
                    target=self.click, args=(total_interval_ms, random_delay_ms)
                )
                self.click_thread.start()
            except ValueError:
                messagebox.showerror(
                    "Invalid Input",
                    "Please enter valid numbers for the intervals and delay.",
                )

    def stop_clicking(self):
        self.clicking = False
        self.stop_event.set()
        if self.click_thread:
            self.click_thread.join()
        self.update_status()

    def click(self, interval_ms, random_delay_ms):
        print("Clicking started", interval_ms, random_delay_ms)
        while not self.stop_event.is_set():
            if self.click_type == "left":
                mouse.click("left")
            elif self.click_type == "right":
                mouse.click("right")
            elif self.click_type == "double_left":
                mouse.click("left")
                sleep(uniform(0.05, 0.2))  # Small delay between clicks
                mouse.click("left")
            elif self.click_type == "double_right":
                mouse.click("right")
                sleep(uniform(0.05, 0.2))  # Small delay between clicks
                mouse.click("right")

            self.click_count += 1
            self.update_status()
            delay = interval_ms + random.uniform(0, random_delay_ms)
            print(delay)
            if self.stop_event.wait(delay / 1000.0):  # Convert milliseconds to seconds
                break

    def update_status(self):
        if self.clicking:
            self.status_label.config(
                text=f"Status: Clicking (Count: {self.click_count})"
            )
        else:
            self.status_label.config(
                text=f"Status: Stopped (Total Clicks: {self.click_count})"
            )

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            self.interval_entry_sec.insert(
                0, config.get("Settings", "interval_sec", fallback="")
            )
            self.interval_entry_ms.insert(
                0, config.get("Settings", "interval_ms", fallback="")
            )
            self.random_delay_entry_ms.insert(
                0, config.get("Settings", "random_delay_ms", fallback="")
            )
            self.hotkey_toggle = config.get("Settings", "hotkey_toggle", fallback="f11")
            self.hotkey_entry.insert(0, self.hotkey_toggle)

            # Load click type
            self.click_type = config.get("Settings", "click_type", fallback="left")
            click_type_map = {
                "left": 0,
                "right": 1,
                "double_left": 2,
                "double_right": 3,
            }
            self.click_type_combo.current(click_type_map.get(self.click_type, 0))

    def save_config(self):
        config = configparser.ConfigParser()
        config["Settings"] = {
            "interval_sec": self.interval_entry_sec.get(),
            "interval_ms": self.interval_entry_ms.get(),
            "random_delay_ms": self.random_delay_entry_ms.get(),
            "hotkey_toggle": self.hotkey_toggle,
            "click_type": self.click_type,
        }
        with open(self.config_file, "w") as configfile:
            config.write(configfile)

    def on_closing(self):
        self.stop_clicking()
        self.save_config()
        self.quit()
        self.destroy()


if __name__ == "__main__":
    try:
        app = AutoClickerApp()
        app.mainloop()
    except KeyboardInterrupt:
        app.stop_clicking()
