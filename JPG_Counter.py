import os
import tkinter as tk
from tkinter import filedialog, messagebox

def browse_scan_folder():
    folder = filedialog.askdirectory(title="Select Folder to Scan")
    if folder:
        scan_entry.delete(0, tk.END)
        scan_entry.insert(0, folder)

def browse_output_folder():
    folder = filedialog.askdirectory(title="Select Output Folder")
    if folder:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder)

def count_jpg_files():
    scan_dir = scan_entry.get().strip()
    output_folder = output_entry.get().strip()
    output_filename = filename_entry.get().strip()

    # Validate inputs
    if not scan_dir or not os.path.isdir(scan_dir):
        messagebox.showerror("Error", "Please select a valid folder to scan.")
        return
    if not output_folder or not os.path.isdir(output_folder):
        messagebox.showerror("Error", "Please select a valid output folder.")
        return
    if not output_filename:
        messagebox.showerror("Error", "Please enter a valid output filename.")
        return

    output_path = os.path.join(output_folder, output_filename)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for root, dirs, files in os.walk(scan_dir):
                jpg_count = sum(1 for file in files if file.lower().endswith(".jpg"))
                f.write(f"{os.path.abspath(root)} | {jpg_count}\n")

        messagebox.showinfo("Success", f"✅ JPG file counts saved to:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("JPG File Counter")
root.geometry("550x400")
root.resizable(False, False)

# Heading
tk.Label(root, text="📸 JPG File Counter", font=("Arial", 16, "bold"), fg="blue").pack(pady=10)

# Scan folder
tk.Label(root, text="Select folder to scan:", font=("Arial", 11)).pack(pady=5)
scan_entry = tk.Entry(root, width=60)
scan_entry.pack(pady=2)
tk.Button(root, text="Browse", command=browse_scan_folder).pack(pady=5)

# Output folder
tk.Label(root, text="Select output folder:", font=("Arial", 11)).pack(pady=5)
output_entry = tk.Entry(root, width=60)
output_entry.pack(pady=2)
tk.Button(root, text="Browse", command=browse_output_folder).pack(pady=5)

# Output file name
tk.Label(root, text="Output file name (e.g. jpg_count.txt):", font=("Arial", 11)).pack(pady=5)
filename_entry = tk.Entry(root, width=40)
filename_entry.pack(pady=2)
filename_entry.insert(0, "jpg_count.txt")

# Run button
tk.Button(root, text="Count JPG Files", command=count_jpg_files,
          bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=15)

root.mainloop()
