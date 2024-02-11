import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pyfiglet
from colorama import Fore, Style
import time

# Import all functions from your code
from BreachProtocol import read_data_from_file, find_maximum_reward, display_grid

class BreachProtocolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Breach Protocol GUI")
        self.root.geometry("400x300")

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill="both")

        # Title label
        self.title_label = tk.Label(self.main_frame, text="Breach Protocol", font=("Helvetica", 16, "bold"), bg="#303030", fg="white")
        self.title_label.pack(pady=10)

        # Filename label
        self.filename_label = tk.Label(self.main_frame, text="Masukkan nama file:", bg="#303030", fg="white")
        self.filename_label.pack()

        # Entry for entering the file name
        self.filename_entry = tk.Entry(self.main_frame, width=30)
        self.filename_entry.pack()

        # Button for browsing the file
        self.browse_button = tk.Button(self.main_frame, text="Cari File", command=self.browse_file, bg="#007ACC", fg="white", relief="flat")
        self.browse_button.pack(pady=5)

        # Button to start the process
        self.start_button = tk.Button(self.main_frame, text="Mulai Proses", command=self.start_process, bg="#4CAF50", fg="white", relief="flat")
        self.start_button.pack(pady=10)

    def browse_file(self):
        # Open a file dialog to select a file and fill the entry with the selected file path
        filename = filedialog.askopenfilename(initialdir="/", title="Pilih File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, filename)

    def start_process(self):
        # Get the file name from the entry
        filename = self.filename_entry.get()

        # Validate if a file name has been entered
        if not filename:
            messagebox.showwarning("Peringatan", "Masukkan nama file terlebih dahulu.")
            return

        try:
            # Read data from the file and start the process
            buffer_size, matrix_width, matrix_height, matrix, sequences_and_rewards = read_data_from_file(filename)
            sorted_sequences = sorted(sequences_and_rewards.items(), key=lambda x: x[1], reverse=True)
            max_buffer, coordinates, max_reward, execution_time = find_maximum_reward(buffer_size, matrix_width, matrix_height, matrix, sorted_sequences)

            # Display the result in the GUI
            self.display_result(max_reward, max_buffer, coordinates, execution_time)

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def display_result(self, max_reward, max_buffer, coordinates, execution_time):
        # Display the result in a message box
        result_text = f"Reward Maksimal: {max_reward}\nIsi Buffer: {max_buffer}\nKoordinat Setiap Token:\n{coordinates}\nWaktu Eksekusi: {execution_time:.3f} ms"
        messagebox.showinfo("Hasil", result_text)


def main():
    root = tk.Tk()
    app = BreachProtocolGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
