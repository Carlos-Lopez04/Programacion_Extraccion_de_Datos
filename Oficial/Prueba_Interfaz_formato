from tkinter import Tk, Frame, Label, Button, BOTH, X, Y, LEFT, RAISED
from tkinter import Canvas
from tkinter import font


# FONDOS Y BASE
COLOR_FONDO = "#0F0F0F"          #
COLOR_BORDE = "#3A3A3A"         
COLOR_PRIMARIO = "#E50914"       
COLOR_SECUNDARIO = "#B81D24"     
COLOR_TERCIARIO = "#6D6D6D"     
COLOR_ACENTO = "#FFD700"        
COLOR_TEXTO = "#FFFFFF"          
COLOR_TEXTO_CLARO = "#000000"    


# Configuración para la ventana
root = Tk()
root.title("TMDB Data Manager - Interactive Edition")
root.geometry("650x550")
root.resizable(True, True)
root.configure(bg=COLOR_FONDO)

# Fuentes de texto
try:
    fuente_titulo = font.Font(family="Helvetica", size=20, weight="bold")
    fuente_subtitulo = font.Font(family="Helvetica", size=12, slant="italic")
    fuente_botones = font.Font(family="Arial", size=12, weight="bold")
    fuente_texto = font.Font(family="Arial", size=10)
except:
    fuente_titulo = font.Font(size=20, weight="bold")
    fuente_subtitulo = font.Font(size=12, slant="italic")
    fuente_botones = font.Font(size=12, weight="bold")
    fuente_texto = font.Font(size=10)

# Frame principal
main_frame = Frame(root, bg=COLOR_FONDO, padx=30, pady=20)
main_frame.pack(fill=BOTH, expand=True)

# Estilo para el encabezado
header_frame = Frame(main_frame, bg=COLOR_PRIMARIO, height=100,
                   highlightbackground=COLOR_ACENTO, highlightthickness=3)
header_frame.pack(fill=X, pady=(0, 20))

# Efecto para el título
label_title = Label(header_frame,
                   text="TMDB Data Manager",
                   font=fuente_titulo,
                   bg=COLOR_PRIMARIO,
                   fg=COLOR_TEXTO_CLARO,
                   padx=20)
label_title.pack(side=LEFT, fill=Y)

# Efecto subtítulo
label_subtitle = Label(header_frame,
                      text="Interactive Professional Edition",
                      font=fuente_subtitulo,
                      bg=COLOR_PRIMARIO,
                      fg="#e9ecef",
                      padx=20)
label_subtitle.pack(side=LEFT, fill=Y)

# Frame de contenido
content_frame = Frame(main_frame,
                     bg="white",
                     highlightbackground=COLOR_BORDE,
                     highlightthickness=1,
                     padx=30,
                     pady=30,
                     relief=RAISED)
content_frame.pack(fill=BOTH, expand=True)

# Widget de ejemplo en el content_frame (para que no quede vacío)
Label(content_frame,
      text="Contenido principal aquí",
      font=fuente_texto,
      bg="white").pack(pady=20)

root.mainloop()
