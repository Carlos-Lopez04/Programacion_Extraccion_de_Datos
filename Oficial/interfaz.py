import requests
import pandas as pd
from tkinter import messagebox

#Colores para los botones de la ventana

COLOR_FONDO = "#f8f9fa"
COLOR_PRIMARIO = "#1d8ecb"
COLOR_SECUNDARIO = "#1149ea"
COLOR_TERCIARIO = "#20c997"
COLOR_ACENTO = "#1d8ecb"
COLOR_PELIGRO = "#dc3545"
COLOR_TEXTO = "#212529"
COLOR_TEXTO_CLARO = "#ffffff"
COLOR_BORDE = "#dee2e6"


#Configuracion para la ventana
root = Tk()
root.title("TMDB Data Manager - Interactive Edition"
root.geometry("650x550")
root.resizable(True, True)
root.configure(bg=COLOR_FONDO)


#Fuentes de texto
try:
    fuente_titulo = font.Font(family = "Helvetica", size=20, weight="bold")
    fuente subtitulo = font.Font(family = "Helvetica", size=20, slant="italic")
    fuente_botones = font.Font(family="Arial", size=12, weight="bold")
    fuente_texto = font.Font(family="Arial", size=10)

except:
    fuente_titulo = font.Font(size=20, weight="bold")
    fuent_subtitulo = font.Font("size=12, slant="italic")
    fuente_botones = font.Font(size=12, weight="bold")
    fuente_texto = font.Font(size=10)


#
main_frame = Frame(root, bg=COLOR_FONDO, padx=30, pady=20)
main_frame.pack(fill= BOTH, expand=True)



#Estilo para el encabezado
header_frame = Frame(main_frame, bg=COLOR_PRIMARIO, height=100,
                     highlightbackground=COLOR_ACENTO, highlightthickness=3)

header_frame.pack(fill=X, pady=(0, 20))


#Efecto para el titulo
label_title = Label(header_frame,
                    text="TMDB Data Manager",
                    font=fuente_titulo,
                    bg=COLOR_PRIMARIO,
                    fg=COLOR_TEXTO_CLARO,
                    padx=20)

label_title.pack(side=LEFT, fill=Y)



#Efecto subtitulo
label_subtitle = Label(header_frame,
                       text="Interactive Professional Edition",
                       font=fuente_subtitulo,
                       bg=COLOR_PRIMARIO,
                       fg="#e9ecef",
                       padx=20)

label_subtitle.pack(side=LEFT, fill=Y)

#Frame
content_frame = Frame(main_frame,
                      bg="white",
                      highlightbackground=COLOR_BORDE,
                      highlightthickness=1,
                      padx=30,
                      pady=30,
                      relief=RAISED)

content_frame.pack(fill=BOTH, expand=True)




