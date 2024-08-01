import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import xarray as xr
import pandas as pd
import os
import threading


def convert_netcdf_to_csv(netcdf_file, output_dir, progress_callback):
    try:
        ds = xr.open_dataset(netcdf_file)
        df = ds.to_dataframe()
        csv_file = os.path.join(
            output_dir, f"{os.path.splitext(os.path.basename(netcdf_file))[0]}.csv"
        )
        df.to_csv(csv_file)
        print(f"Saved {csv_file}")
        progress_callback()
    except Exception as e:
        print(f"Failed to convert {netcdf_file}: {e}")


def process_files(input_dir, output_dir, progress_callback):
    files = [
        os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".nc")
    ]
    total_files = len(files)
    for i, file in enumerate(files):
        convert_netcdf_to_csv(
            file, output_dir, lambda: progress_callback(i + 1, total_files)
        )


def start_conversion():
    input_dir = input_path_var.get()
    output_dir = output_path_var.get()
    if not input_dir or not output_dir:
        messagebox.showwarning(
            "Input Error", "Please select both input and output directories."
        )
        return

    progress_bar["value"] = 0
    progress_label["text"] = "Starting conversion..."

    def run_conversion():
        process_files(input_dir, output_dir, update_progress)

        progress_bar["value"] = 100
        progress_label["text"] = "Conversion completed successfully!"
        messagebox.showinfo("Success", "Conversion completed successfully!")

    # Run the conversion in a separate thread
    threading.Thread(target=run_conversion).start()


def update_progress(current, total):
    progress = (current / total) * 100
    progress_bar["value"] = progress
    progress_label["text"] = f"Progress: {current}/{total} files"


def browse_input_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        input_path_var.set(folder_selected)


def browse_output_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_path_var.set(folder_selected)


# Create the main window
root = tk.Tk()
root.title("NCDF to CSV")

# Create and place widgets
tk.Label(root, text="NCDF to CSV Converter", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Input Directory:").pack(pady=5)
input_path_var = tk.StringVar()
tk.Entry(root, textvariable=input_path_var, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=browse_input_directory).pack(pady=5)

tk.Label(root, text="Output Directory:").pack(pady=5)
output_path_var = tk.StringVar()
tk.Entry(root, textvariable=output_path_var, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=browse_output_directory).pack(pady=5)

tk.Button(root, text="Start Conversion", command=start_conversion).pack(pady=20)

# Create and place progress bar and label
progress_bar = ttk.Progressbar(
    root, orient="horizontal", length=400, mode="determinate"
)
progress_bar.pack(pady=10)
progress_label = tk.Label(root, text="Progress: 0/0 files")
progress_label.pack(pady=5)

root.mainloop()
