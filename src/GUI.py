# Nama : Atqiya Haydar Luqman
# NIM : 13522163
# Kelas : K3

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from colorama import Fore, Style

from BreachProtocol import read_data_from_file, find_maximum_reward, display_grid, save_output_to_file

class BreachProtocolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Breach Protocol GUI")
        self.root.geometry("650x400")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, fill="both")

        # Judul
        self.title_label = tk.Label(self.main_frame, text="Breach Protocol", font=("Helvetica", 20, "bold"), fg="black")
        self.title_label.pack(pady=10)

        # Subjudul
        self.subtitle_label = tk.Label(self.main_frame, text="Tucil 1 IF2211 Strategi Algoritma", font=("Helvetica", 12), fg="black")
        self.subtitle_label.pack(pady=5)

        # Label masukkan file
        self.filename_label = tk.Label(self.main_frame, text="Masukkan nama file:", fg="black", font=("Helvetica", 10))
        self.filename_label.pack(pady=8)

        # Input nama file
        self.filename_entry = tk.Entry(self.main_frame, width=30)
        self.filename_entry.pack(pady=5)

        # Tombol mencari file
        self.browse_button = tk.Button(self.main_frame, text="Cari File", command=self.browse_file, font=("Helvetica", 10, "bold"), bg="#7F27FF", fg="white", relief="flat")
        self.browse_button.pack(pady=10)

        # Tombol memulai proses
        self.start_button = tk.Button(self.main_frame, text="Mulai Proses", command=self.start_process, bg="#FF8911", fg="white", relief="flat", font=("Helvetica", 10, "bold"))
        self.start_button.pack(pady=10)

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Pilih File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        self.filename_entry.delete(0, tk.END)
        self.filename_entry.insert(0, filename)

    def start_process(self):
        filename = self.filename_entry.get()

        if not filename:
            messagebox.showwarning("Peringatan", "Masukkan nama file terlebih dahulu.")
            return

        try:
            buffer_size, matrix_width, matrix_height, matrix, sequences_and_rewards = read_data_from_file(filename)
            sorted_sequences = sorted(sequences_and_rewards.items(), key=lambda x: x[1], reverse=True)
            max_buffer, coordinates, max_reward, execution_time = find_maximum_reward(buffer_size, matrix_width, matrix_height, matrix, sorted_sequences)

            self.display_result(max_reward, max_buffer, coordinates, execution_time, matrix)

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

    def display_result(self, max_reward, max_buffer, coordinates, execution_time, matrix):
        result_text = f"Reward Maksimal: {max_reward}\nIsi Buffer: {max_buffer}\nKoordinat Setiap Token:\n{coordinates}\nWaktu Eksekusi: {execution_time:.3f} ms"
        messagebox.showinfo("Hasil", result_text)

        # Menambahkan tombol Simpan ke File
        save_button = tk.Button(self.root, text="Simpan ke File", command=lambda: self.save_to_file(max_reward, max_buffer, coordinates, execution_time, matrix))
        save_button.pack(pady=5)

    def save_to_file(self, max_reward, max_buffer, coordinates, execution_time, matrix):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            try:
                save_output_to_file(filename, max_reward, max_buffer, coordinates, matrix, execution_time)
                messagebox.showinfo("Sukses", f"Data berhasil disimpan ke file {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan file: {str(e)}")

def main():
    root = tk.Tk()
    app = BreachProtocolGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()