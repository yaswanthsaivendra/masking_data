import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk  

class SimpleGUI:
    def __init__(self, master, start_masking_func):
        self.master = master
        master.title("PIVONY")
        self.start_masking_func = start_masking_func

        # Title
        title_label = tk.Label(master, text="PIVONY Masking Algorithm", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Text under the title
        text_label = tk.Label(master, text="This program reads all CSV, XLS, XLSX files in \n the C:\Windows\\tmp, runs the Python code, and \n generates output files under the same directory")
        text_label.grid(row=1, column=0, columnspan=2, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=(4, 3), relief="flat", background="white", foreground="black",
                        borderwidth=5, focuscolor="none", bordercolor="black", borderradius=10)
        start_button = ttk.Button(master, text="Start", command=self.start_masking_func, style="TButton")
        start_button.grid(row=2, column=1, sticky="e", pady=10, padx=20)

        # Logs
        logs_label = tk.Label(master, text="Console Log", anchor='w')  # 'w' stands for west (left)
        logs_label.grid(row=3, column=0, columnspan=2, pady=5, padx=20, sticky='w')

        self.logs_text = scrolledtext.ScrolledText(master, height=5, width=40)
        self.logs_text.grid(row=4, column=0, columnspan=2, padx=20, pady=10)




