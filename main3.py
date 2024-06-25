import tkinter as tk
from tkinter import ttk
import pyautogui
import pyperclip
import pygetwindow as gw
from datetime import datetime

# Lista de colores para los botones
button_colors = ['#FF5733', '#2ADFAD','#33FF57', '#5733FF', '#33FFFF', '#FFCFAA', '#33AFFA',  '#3CCFFF',]

def get_focused_window():
    return gw.getWindowsWithTitle(gw.getActiveWindow().title)[0]

def read_button_text_from_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def write_to_active_window(text):
    active_window = get_focused_window()
    active_window.activate()
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press(' ') 

    app.after(100, show_main_window)

    # Enfocar el cuadro de texto en la ventana externa después de escribir el texto
    try:
        text_widget = active_window.widget(text='Text')
        text_widget.focus()
    except tk.TclError:
        print("Error: No se pudo encontrar el cuadro de texto en la ventana externa.")



def on_copy_button_click2(ttt):
    # Ocultar temporalmente la ventana de la aplicación
    app.withdraw()

    write_to_active_window(ttt)

    # Volver a mostrar la ventana de la aplicación después de la escritura
    app.deiconify()

def on_copy_button_click():
    current_time = datetime.now().strftime('%H:%M:%S')
    # Ocultar temporalmente la ventana de la aplicación
    app.withdraw()

    write_to_active_window(current_time)

    # Volver a mostrar la ventana de la aplicación después de la escritura
    app.deiconify()


def select_all_text():
      # Ocultar temporalmente la ventana de la aplicación
    app.withdraw()
    active_window = get_focused_window()
    active_window.activate()
    pyautogui.hotkey('ctrl', 'e')
    pyautogui.press('backspace')  # Emular la pulsación de la tecla "Retroceso" para borrar el espacio

 # Volver a mostrar la ventana de la aplicación después de la escritura
    app.deiconify()


def show_main_window():
    app.deiconify()

app = tk.Tk()
app.title('Aplicación de Escritorio')
app.geometry('500x400')  # Ajusta el tamaño según tus preferencias
app.grid_rowconfigure(0, weight=1)  # Hacer que la fila 0 se expanda verticalmente
app.grid_columnconfigure(0, weight=7)  # Hacer que la columna 0 ocupe el 70% del ancho disponible
app.grid_columnconfigure(1, weight=3)  # Hacer que la columna 1 ocupe el 30% del ancho disponible

# Utilizar el tema visual de Windows 10 u 11
style = ttk.Style(app)
style.theme_use('vista')  # O 'vista' para un tema más antiguo

# Crear el Frame principal
main_frame = ttk.Frame(app)
main_frame.grid(row=0, column=0, sticky='nsew')
main_frame.grid_rowconfigure(0, weight=1)  # Hacer que la fila 0 se expanda verticalmente
main_frame.grid_columnconfigure(0, weight=1)  # Hacer que la columna 0 se expanda horizontalmente

# Crear el primer Canvas para mostrar los botones
canvas1 = tk.Canvas(main_frame, bg='white')
canvas1.grid(row=0, column=0, sticky='nsew')  # Hacer que el Canvas1 ocupe todo el espacio disponible

# Frame para contener los botones dinámicos
button_frame = ttk.Frame(canvas1)
canvas1.create_window((0, 0), window=button_frame, anchor=tk.NW)

# Crear un widget de desplazamiento vertical para el primer Canvas
scrollbar_y1 = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas1.yview)
scrollbar_y1.grid(row=0, column=1, sticky='ns')  # Ubicar el Scrollbar1 a la derecha del Canvas1

# Vincular el widget de desplazamiento al primer Canvas
canvas1.configure(yscrollcommand=scrollbar_y1.set)





# Leer el contenido del archivo lista.txt y crear botones
button_texts = read_button_text_from_file('lista.txt')
for index, text in enumerate(button_texts):
#for text in button_texts:
    text_to_write, button_text = text.strip().split("|")
    button_text = button_text.strip()
    if button_text:
        # Seleccionar un color diferente para cada botón según el índice
        button_color = button_colors[index % len(button_colors)]
        button = ttk.Button(button_frame, text=button_text,  command=lambda r=text_to_write: on_copy_button_click2(r))
        button.pack(pady=5)

      


copy_button = ttk.Button(button_frame, text='Escribir hora actual en ventana enfocada', command=on_copy_button_click)
copy_button.pack(pady=10)

copy_button2 = ttk.Button(button_frame, text='Copiar texto específico', command=lambda: on_copy_button_click2('Texto específico a copiar'))
copy_button2.pack(pady=30)

# Botón para seleccionar todo el texto en la ventana externa
select_all_button = ttk.Button(button_frame, text='Seleccionar Todo', command=select_all_text)
select_all_button.pack(pady=10)


# Configurar el desplazamiento del canvas para adaptarse a los contenidos
button_frame.update_idletasks()  # Actualizar el frame antes de configurar el desplazamiento
canvas1.config(scrollregion=canvas1.bbox("all"))









# Crear el segundo Canvas para mostrar la lista externa
canvas2 = tk.Canvas(main_frame, bg='white')
canvas2.grid(row=0, column=2, sticky='nsew')  # Hacer que el Canvas2 ocupe todo el espacio disponible

# Frame para contener los elementos de la lista
list_frame = ttk.Frame(canvas2)
canvas2.create_window((0, 0), window=list_frame, anchor=tk.NW)

# Crear un widget de desplazamiento vertical para el segundo Canvas
scrollbar_y2 = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas2.yview)
scrollbar_y2.grid(row=0, column=3, sticky='ns')  # Ubicar el Scrollbar2 a la derecha del Canvas2

# Vincular el widget de desplazamiento al segundo Canvas
canvas2.configure(yscrollcommand=scrollbar_y2.set)

# Leer el contenido del archivo personal.txt y agregar etiquetas en el segundo Canvas
def read_personal_data(filename):
    with open(filename, 'r') as file:
        return file.readlines()

personal_data = read_personal_data('personal.txt')
for data in personal_data:
    data = data.strip()
    if data:
        label = ttk.Label(list_frame, text=data)
        label.pack(pady=5)

# Configurar el desplazamiento del segundo Canvas para adaptarse a los contenidos
list_frame.update_idletasks()  # Actualizar el frame antes de configurar el desplazamiento
canvas2.config(scrollregion=canvas2.bbox("all"))




# Establecer el atributo "topmost" de la ventana en True
app.wm_attributes("-topmost", True)

# Volver a mostrar la ventana principal después de un tiempo para evitar que se quede escondida si algo falla
app.after(1000, show_main_window)

app.mainloop()
