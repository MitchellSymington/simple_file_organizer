import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, shutil

# === Application Setup ===
app = tk.Tk()
app.overrideredirect(True)  # Hide native title bar
app.update_idletasks()

# Set fixed window size and center it on screen
width, height = 360, 240
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2)
app.geometry(f"{width}x{height}+{x}+{y}")
app.resizable(False, False)

# === Window Dragging Support ===
x_offset = y_offset = 0

def start_move(event):
    global x_offset, y_offset
    x_offset, y_offset = event.x, event.y

def do_move(event):
    app.geometry(f"+{event.x_root - x_offset}+{event.y_root - y_offset}")

def close_window():
    app.destroy()

def minimize_window():
    app.overrideredirect(False)
    app.iconify()

def restore_window(event):
    app.overrideredirect(True)

app.bind("<Map>", restore_window)

# === Colors ===
TITLE_COLOR = "#007fff"
HOVER_COLOR = "#005bb5"
ERROR_COLOR = "#d32f2f"

# === Title Bar ===
title_bar = tk.Frame(app, bg=TITLE_COLOR, height=30)
title_bar.pack(fill="x")
title_bar.bind("<ButtonPress-1>", start_move)
title_bar.bind("<B1-Motion>", do_move)

tk.Label(
    title_bar,
    text="File Organizer",
    bg=TITLE_COLOR,
    fg="white",
    font=("Helvetica", 10, "bold")
).pack(side="left", padx=10)

# Hover effect utility
def add_hover(widget, normal_bg, hover_bg):
    widget.bind("<Enter>", lambda e: widget.config(bg=hover_bg))
    widget.bind("<Leave>", lambda e: widget.config(bg=normal_bg))

# === Title Bar Buttons ===
close_btn = tk.Button(title_bar, text="✕", command=close_window, bd=0, bg=TITLE_COLOR, fg="white")
close_btn.pack(side="right")
add_hover(close_btn, TITLE_COLOR, ERROR_COLOR)

help_btn = tk.Button(
    title_bar, text="?", bd=0, bg=TITLE_COLOR, fg="white",
    command=lambda: messagebox.showinfo("Help", "1. Select a folder\n2. Choose options\n3. Click 'Organize Files' to proceed.")
)
help_btn.pack(side="right")
add_hover(help_btn, TITLE_COLOR, HOVER_COLOR)

minimize_btn = tk.Button(title_bar, text="━", command=minimize_window, bd=0, bg=TITLE_COLOR, fg="white")
minimize_btn.pack(side="right")
add_hover(minimize_btn, TITLE_COLOR, HOVER_COLOR)

# === Main Frame ===
main_container = tk.Frame(app)
main_container.pack(fill="both", expand=True)

folder_var = tk.StringVar()
move_var = tk.IntVar(value=1)
status_var = tk.StringVar()

# === Folder Selection ===
folder_frame = tk.Frame(main_container)
folder_frame.pack(fill="x", padx=10, pady=(15, 5))
tk.Label(folder_frame, text="Folder:").pack(side="left")
tk.Entry(folder_frame, textvariable=folder_var, width=25).pack(side="left", padx=(5, 0))
tk.Button(folder_frame, text="📁", command=lambda: folder_var.set(filedialog.askdirectory() or folder_var.get())).pack(side="left", padx=5)

# === Options Section ===
options_frame = tk.LabelFrame(main_container, text="Options")
options_frame.pack(fill="x", padx=10, pady=5)

action_row = tk.Frame(options_frame)
action_row.pack(anchor="w", padx=10, pady=5)
tk.Label(action_row, text="Action:").pack(side="left")
tk.Radiobutton(action_row, text="Move", variable=move_var, value=1).pack(side="left", padx=5)
tk.Radiobutton(action_row, text="Copy", variable=move_var, value=0).pack(side="left", padx=5)

# === Organize Button ===
tk.Frame(main_container, height=10).pack()
organize_btn = tk.Button(
    main_container,
    text="Organize Files",
    height=2,
    width=36,
    bg=TITLE_COLOR,
    fg="white",
    activebackground=HOVER_COLOR,
    activeforeground="white",
    font=("Helvetica", 10, "bold"),
    command=lambda: organize_files()
)
organize_btn.pack(padx=10, pady=(5, 10))
add_hover(organize_btn, TITLE_COLOR, HOVER_COLOR)

status_label = tk.Label(main_container, textvariable=status_var, anchor="w")
status_label.pack(anchor="w", padx=10, pady=(0, 10))

# === File Organization Logic ===
def organize_files():
    folder = folder_var.get()
    if not folder:
        status_var.set("Error: Please select a folder.")
        status_label.config(fg="red")
        return

    status_var.set("Processing...")
    status_label.config(fg="black")
    app.update_idletasks()

    try:
        import time
        time.sleep(1)  # Simulate processing time

        count = 0
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1].lower()
                if ext:
                    target_folder = os.path.join(folder, ext[1:])
                    os.makedirs(target_folder, exist_ok=True)
                    dest_path = os.path.join(target_folder, filename)
                    if move_var.get() == 1:
                        shutil.move(filepath, dest_path)
                    else:
                        shutil.copy2(filepath, dest_path)
                    count += 1

        status_var.set(f"Done. {count} files organized.")
        status_label.config(fg="green")
    except Exception as e:
        status_var.set(f"Error: {str(e)}")
        status_label.config(fg="red")

# === Launch Application ===
app.mainloop()
