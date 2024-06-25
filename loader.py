import tkinter as tk
from tkinter import ttk
import threading
import subprocess

def main_window():
    subprocess.call(["python", "main.py"])  # Llama al archivo main.py

def close_preloader(preloader):
    preloader.destroy()

def create_preloader():
    preloader = tk.Tk()
    preloader.title('Cargando...')
    preloader.geometry('300x100')
    
    label = ttk.Label(preloader, text="Cargando la aplicación...", font=('Arial', 12))
    label.pack(pady=30)
    
    preloader.after(2000, main_window)  # Simulando una carga de 2 segundos
    
    preloader.mainloop()

# Crear un hilo para el preloader
preloader_thread = threading.Thread(target=create_preloader)
preloader_thread.start()
