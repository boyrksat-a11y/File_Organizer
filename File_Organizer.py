import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def browse_input():
    path = filedialog.askdirectory(title="Select Input Folder")
    input_entry.delete(0, tk.END)
    input_entry.insert(0, path)

def browse_output():
    path = filedialog.askdirectory(title="Select Output Folder")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, path)

def organize_files():
    input_path = input_entry.get().strip()
    output_path = output_entry.get().strip()
    main_folder = main_entry.get().strip()
    batch_text = batch_textbox.get("1.0", tk.END).strip()
    mapping_mode = mapping_var.get()

    # --- Validation ---
    if not input_path or not os.path.isdir(input_path):
        messagebox.showerror("Error", "Please select a valid input folder.")
        return
    if not output_path or not os.path.isdir(output_path):
        messagebox.showerror("Error", "Please select a valid output folder.")
        return

    # Create main folder if specified
    if main_folder:
        output_path = os.path.join(output_path, main_folder)
        os.makedirs(output_path, exist_ok=True)

    if mapping_mode:
        # ---------------- CSV MAPPING MODE ----------------
        csv_files = [f for f in os.listdir(input_path) if f.lower().endswith(".csv")]
        if not csv_files:
            messagebox.showinfo("No CSV Files", "No CSV files found in the input folder.")
            return

        if not batch_text:
            messagebox.showerror("Error", "Please enter Batch Names.")
            return

        lines = [line.strip() for line in batch_text.splitlines() if line.strip()]
        count = 0

        for line in lines:
            if "|" in line:
                # Handle pipe-based folder naming
                main_part, sub_part = line.split("|", 1)
                main_folder_path = os.path.join(output_path, main_part)
                os.makedirs(main_folder_path, exist_ok=True)
                sub_folder = os.path.join(main_folder_path, sub_part)
                os.makedirs(sub_folder, exist_ok=True)
                for file in csv_files:
                    shutil.copy(os.path.join(input_path, file), os.path.join(sub_folder, file))
                count += 1
            else:
                # Handle simple folder naming
                folder_name = line
                new_folder = os.path.join(output_path, folder_name)
                os.makedirs(new_folder, exist_ok=True)
                for file in csv_files:
                    shutil.copy(os.path.join(input_path, file), os.path.join(new_folder, file))
                count += 1

        messagebox.showinfo("Success", f"Created {count} folders and copied CSV files successfully!")

    else:
        # ---------------- TEXT MODE ----------------
        txt_files = [f for f in os.listdir(input_path) if f.lower().endswith(".txt")]
        if not txt_files:
            messagebox.showinfo("No Files", "No text files found in the input folder.")
            return

        for file in txt_files:
            file_name = os.path.splitext(file)[0]
            new_folder = os.path.join(output_path, file_name)
            os.makedirs(new_folder, exist_ok=True)
            shutil.copy(os.path.join(input_path, file), os.path.join(new_folder, file))

        messagebox.showinfo("Success", f"Processed {len(txt_files)} text files successfully!")


# ---------------- GUI ----------------
root = tk.Tk()
root.title("File Organizer")
root.geometry("600x550")
root.resizable(False, False)

# Input Path
tk.Label(root, text="Input Folder:").pack(pady=5)
input_entry = tk.Entry(root, width=60)
input_entry.pack()
tk.Button(root, text="Browse", command=browse_input).pack(pady=5)

# Output Path
tk.Label(root, text="Output Folder:").pack(pady=5)
output_entry = tk.Entry(root, width=60)
output_entry.pack()
tk.Button(root, text="Browse", command=browse_output).pack(pady=5)

# Main Folder (optional)
tk.Label(root, text="Main Folder Name (optional):").pack(pady=5)
main_entry = tk.Entry(root, width=60)
main_entry.pack()

# Mapping Mode Checkbox
mapping_var = tk.BooleanVar()
mapping_checkbox = tk.Checkbutton(root, text="Mapping (Use CSV Mode)", variable=mapping_var)
mapping_checkbox.pack(pady=5)

# Batch Name text box (only used in Mapping Mode)
tk.Label(root, text="Batch Name (one per line or use pipe '|' for nested folders):").pack(pady=5)
batch_textbox = scrolledtext.ScrolledText(root, width=70, height=10)
batch_textbox.pack(pady=5)

# Run Button
tk.Button(root, text="Organize Files", command=organize_files, bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=15)

root.mainloop()
