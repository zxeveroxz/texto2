import tkinter as tk
from tkinter import messagebox 
from tkinter import ttk
import pyperclip
import pyautogui
import pygetwindow
from ttkbootstrap import Style
import textwrap  # Añade esta línea para importar textwrap
import locale
import os
import socket
import threading

# Configuración del socket
ip = '1.2.1.42'  # Escucha en todas las interfaces
port = 8080


class ClaseCliente():

    def __init__(self):
        print("Conectando el socket cliente")
        self.nick = "zeta"

        try:
            # Configuramos el tipo de conexión y nos conectamos al servidor.
            self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente.connect(('1.2.1.42', 8080))  # Cambia la dirección IP y el puerto según tu servidor

            # Ponemos un thread a recibir los mensajes.
            mensajeRecibido = threading.Thread(target=self.RecibirMensajes)
            mensajeRecibido.daemon = True
            mensajeRecibido.start()

            # Bucle que permite enviar mensajes
            while True:
                mensaje = "holasssssssss"
                try:
                    if mensaje != "salir":
                        self.EnviarMensajes(mensaje)
                    else:
                        self.cliente.close()
                        break
                except Exception as e:
                    print("Error al enviar mensaje:", e)
                    self.cliente.close()
                    break

        except ConnectionRefusedError:
            print("No se pudo conectar al servidor. Asegúrate de que el servidor esté en línea.")
            return

    def RecibirMensajes(self):
        while True:
            try:
                mensaje = self.cliente.recv(2048)
                print("Mensaje recibido del servidor:", mensaje.decode())
            except Exception as e:
                print("Error al recibir mensaje:", e)
                self.cliente.close()
                break

    def EnviarMensajes(self, mensaje):
        mensaje = self.nick + "- " + mensaje
        self.cliente.send(bytes(mensaje.encode()))  # Enviamos el mensaje codificado al servidor

# --------------------------------------------------------------#

#start = ClaseCliente()


def main():

    last_focused_window = None


    mouse_over_button = False
    mouse_over_app = False

    def hide_button(button):
        #messagebox.showinfo("Alerta", "Este es un mensaje de alerta. "+ button.canvas)
        button.pack_forget()  # Oculta el botón del layout

    def update_canvas_scrollregion(canvas):
        canvas.update_idletasks()  # Asegúrate de que todos los widgets estén correctamente actualizados
        bbox = canvas.bbox("all")  # Obtén las coordenadas de todos los widgets en el canvas
        canvas.config(scrollregion=bbox)  # Actualiza la scrollregion del canvas
        # Ajusta el tamaño del scrollbar de acuerdo a la cantidad de botones visibles
        visible_buttons = [button for button in canvas.winfo_children() if button.winfo_ismapped()]
        total_buttons = len(canvas.winfo_children())
        
        if canvas == canvas1:
            scrollbar1.set(0, len(visible_buttons) / total_buttons)  # Aquí debes usar el scrollbar del canvas correspondiente
        else:
            scrollbar2.set(0, len(visible_buttons) / total_buttons)  # Aquí debes usar el scrollbar del canvas correspondiente


    def on_canvas1_configure(event):
        canvas1.configure(scrollregion=canvas1.bbox("all"))

    def on_canvas2_configure(event):
        canvas2.configure(scrollregion=canvas2.bbox("all"))

    def read_file_content(filename):
        if not os.path.exists(filename):
            # Si el archivo no existe, créalo y dale permiso de escritura
            with open(filename, 'w') as file:
                pass  # Puedes agregar contenido inicial si lo deseas
        with open(filename, 'r') as file:
        # os.chmod(filename, 0o666) 
            return file.readlines()


    def create_buttons(canvas, text_list):
        button_frame = ttk.Frame(canvas)
        canvas.create_window((canvas.winfo_width() / 2, canvas.winfo_height() / 2), window=button_frame)
        #canvas.create_window((canvas.winfo_width() / 2, canvas.winfo_height() / 2), anchor='nw', window=button_frame, width=canvas.winfo_width(), height=canvas.winfo_height())

        # Crear botones en el canvas
        for i, line in enumerate(text_list):
            parts = line.strip().split('|')
            if len(parts) == 2:
                alert_text, button_text = parts
            else:
                button_text = line.strip()
                alert_text = ""
            button = ttk.Button(button_frame, text=button_text, width=20, command=lambda text=alert_text: on_button_click(text))
            button.canvas = canvas
            
            # Expandir horizontalmente el botón en el canvas
            button.pack(fill=tk.X, padx=7, pady=5)

            # Ajustar texto del botón si es demasiado largo
            if len(button_text) > 25:  # Cambiar 10 al valor deseado
                wrapped_text = '\n'.join(textwrap.wrap(button_text, width=20))  # Cambiar 10 al valor deseado
                button.config(text=wrapped_text)

            button.bind("<Button-3>", lambda event, b=button: (hide_button(b), update_canvas_scrollregion(b.canvas)))
            button.bind("<Enter>", lambda event, text=alert_text: show_tooltip(event, text),button.configure(cursor="hand2"))
            button.bind("<Leave>", hide_tooltip)
        

    def create_buttons_horizontal(canvas, text_list):

        
        x_position = 10
        for line in text_list:
            parts = line.strip().split('|')
            if len(parts) == 2:
                alert_text, button_text = parts

                key_combination = alert_text.strip()
                keys = key_combination.split('+')
                alert_text = [key.lower() for key in keys]

            else:
                button_text = line.strip()
                alert_text = ""

        
            button = ttk.Button(canvas, text=button_text, style='My.TButton', command=lambda text=alert_text: on_button_click2(text))
            button.place(x=x_position, y=13, width=100, height=36)  # Ajusta los valores según tu diseño
            x_position += 110  # Incrementa la posición para el siguiente botón

            


    def on_button_click2(text):
        print("Botón presionado:", text)
        
        global last_focused_window

        app.withdraw()
        pyautogui.hotkey(*text)  # Emular la combinación de teclas
        last_focused_window = pygetwindow.getWindowsWithTitle(pygetwindow.getActiveWindow().title)[0]
        app.deiconify()

        # Restaurar el foco a la última ventana activa
        if last_focused_window:
            last_focused_window.activate()



    def on_button_click(text):
        global last_focused_window

        # Copiar el texto al portapapeles
        pyperclip.copy(text)
        # Ocultar temporalmente la aplicación
        app.withdraw()
        # Emular la combinación de teclas "Ctrl + V" para pegar el texto en la ventana activa
        pyautogui.hotkey('ctrl', 'v')
    # Obtener la ventana activa antes de ocultar la aplicación
        last_focused_window = pygetwindow.getWindowsWithTitle(pygetwindow.getActiveWindow().title)[0]
        print(last_focused_window)
        # Mostrar la aplicación después de la escritura
        app.deiconify()

        # Restaurar el foco a la última ventana activa
        if last_focused_window:
            last_focused_window.activate()

    def on_canvas1_mousewheel(event):
        canvas1.yview_scroll(-1 * (event.delta // 120), "units")

    def on_canvas2_mousewheel(event):
        canvas2.yview_scroll(-1 * (event.delta // 120), "units")




    def on_button_enter(event):
        global mouse_over_button
        mouse_over_button = True
        if not mouse_over_app:
            app.attributes('-topmost', False)

    def on_button_leave(event):
        global mouse_over_button
        mouse_over_button = False
        if not mouse_over_app:
            app.attributes('-topmost', True)

    def on_app_enter(event):
        global mouse_over_app
        mouse_over_app = True
        if not mouse_over_button:
            app.attributes('-topmost', False)

    def on_app_leave(event):
        global mouse_over_app
        mouse_over_app = False
        if not mouse_over_button:
            app.attributes('-topmost', True)

    def show_tooltip(event, text):
        tooltip = tk.Toplevel(app)
        tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        tooltip.overrideredirect(True)
        label = tk.Label(tooltip, text=text, bg="white", borderwidth=10, relief="solid")
        label.pack()

        label.bind("<Enter>", on_button_enter)
        label.bind("<Leave>", on_button_leave)

        app.bind("<Enter>", on_app_enter)
        app.bind("<Leave>", on_app_leave)

    def hide_tooltip(event):
        for widget in app.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()







    # Crear la ventana principal
    app = tk.Tk()
    app.title('SEDAPAL - TEXTOS RAPIDOS - SERGIO ZEGARRA')
    app.geometry('470x500')
    app.resizable(False, True)


    #app.iconbitmap(BASE64_ICON) 


    # Obtener la resolución del monitor
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Establecer el tamaño máximo de la ventana al 70% de la resolución del monitor
    max_width = int(screen_width * 0.7)
    max_height = int(screen_height * 0.7)
    app.maxsize(max_width, max_height)


    # Crear Canvas superior
    top_canvas = tk.Canvas(app, bg='#000', width=max_width, height=60)
    top_canvas.pack(fill=tk.BOTH, expand=True)


    # Primer Canvas con 230 de ancho
    canvas1 = tk.Canvas(app, width=230, height=max_height)
    canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configurar el Scrollbar para el primer Canvas
    scrollbar1 = ttk.Scrollbar(app, orient=tk.VERTICAL, command=canvas1.yview)
    scrollbar1.pack(side=tk.LEFT, fill=tk.Y)
    canvas1.configure(yscrollcommand=scrollbar1.set)
    canvas1.bind('<Configure>', on_canvas1_configure)

    # Leer el contenido del archivo acciones.txt
    acciones_text_list = read_file_content('acciones.txt')

    # Crear botones en el primer Canvas con el contenido del archivo acciones.txt
    create_buttons(canvas1, acciones_text_list)

    # Vincular el evento de rueda de mouse para el primer Canvas
    canvas1.bind("<Enter>", lambda event: canvas1.bind_all("<MouseWheel>", on_canvas1_mousewheel))
    canvas1.bind("<Leave>", lambda event: canvas1.unbind_all("<MouseWheel>"))

    # Segundo Canvas con 180 de ancho
    canvas2 = tk.Canvas(app, width=220, height=max_height, bg='gray')
    canvas2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configurar el Scrollbar para el segundo Canvas
    scrollbar2 = ttk.Scrollbar(app, orient=tk.VERTICAL, command=canvas2.yview)
    scrollbar2.pack(side=tk.LEFT, fill=tk.Y)
    canvas2.configure(yscrollcommand=scrollbar2.set)
    canvas2.bind('<Configure>', on_canvas2_configure)

    # Leer el contenido del archivo personal.txt
    personal_text_list = read_file_content('personal.txt')

    # Crear botones en el segundo Canvas con el contenido del archivo personal.txt
    create_buttons(canvas2, personal_text_list)

    # Vincular el evento de rueda de mouse para el segundo Canvas
    canvas2.bind("<Enter>", lambda event: canvas2.bind_all("<MouseWheel>", on_canvas2_mousewheel))
    canvas2.bind("<Leave>", lambda event: canvas2.unbind_all("<MouseWheel>"))



    #crear botones para  el canvas top
    buttons_text = [
        "Win+Shift+S|CAPTURAR",
        "Ctrl+C|COPIAR",
        "Ctrl+V|PEGAR",
        "Ctrl+A|SELECC.",
        # Agrega más botones aquí
    ]

    create_buttons_horizontal(top_canvas, buttons_text)


    app.configure(bg='#fdfd61')

    style = ttk.Style(app)
    style = Style(theme='darkly')  # Elige el tema deseado
    app.configure(bg='black') 
    style.configure('TButton', font=('Arial', 10))  
    style.configure('My.TButton', font=('Arial', 8))
    # Cambiar el color de fondo de los canvas en el estilo
    style.configure('TFrame', background='#d8d7d7')  # Cambia el color de fondo según tus preferencias


    app.attributes('-topmost', True)


    app.mainloop()


# Ejecuta el hilo del cliente en segundo plano
#cliente_thread = threading.Thread(target=ClaseCliente)
#cliente_thread.daemon = True  # Permite que el hilo se detenga cuando el programa principal finalice
#cliente_thread.start()


# Ejecuta tu código principal
if __name__ == "__main__":
    main()
