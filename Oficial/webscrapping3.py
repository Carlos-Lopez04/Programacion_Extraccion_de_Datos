import requests
import pandas as pd
import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox, font

API_KEY = "6e9456bdd4ec35e91f83f2cf2950e4c2"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_tmdb_data(endpoint, pages=5):
    all_results = []
    for page in range(1, pages + 1):
        params = {"api_key": API_KEY, "page": page}
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get("results", []))
        else:
            messagebox.showerror("Error", f"Error en página {page}: {response.status_code}")
            break
    return all_results

def to_dataframe(data, content_type):
    df = pd.DataFrame(data)
    df["type"] = content_type
    if content_type == "movie":
        df["title"] = df["title"]
        df["release_date"] = df["release_date"]
    else:
        df["title"] = df["name"]
        df["release_date"] = df["first_air_date"]
    return df[["id", "title", "vote_average", "popularity", "release_date", "type"]]

def hacer_scraping():
    popular_movies = fetch_tmdb_data("/movie/popular")
    top_rated_movies = fetch_tmdb_data("/movie/top_rated")
    popular_series = fetch_tmdb_data("/tv/popular")

    df_popular_movies = to_dataframe(popular_movies, "movie")
    df_top_rated_movies = to_dataframe(top_rated_movies, "movie")
    df_popular_series = to_dataframe(popular_series, "tv")

    df_popular_movies.to_csv("popular_movies.csv", index=False)
    df_top_rated_movies.to_csv("top_rated_movies.csv", index=False)
    df_popular_series.to_csv("popular_series.csv", index=False)

    messagebox.showinfo("Scraping OK", "Scraping completado y CSV guardados.")

def crear_bd_y_cargar():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS tmdb_db")
        conn.database = "tmdb_db"

        cursor.execute("DROP TABLE IF EXISTS movies_popular")
        cursor.execute("DROP TABLE IF EXISTS tv_popular")
        cursor.execute("DROP TABLE IF EXISTS combined_popular")

        cursor.execute("""
            CREATE TABLE movies_popular (
                id INT PRIMARY KEY,
                title VARCHAR(255),
                vote_average FLOAT,
                popularity FLOAT,
                release_date DATE,
                type VARCHAR(10)
            )
        """)

        cursor.execute("""
            CREATE TABLE tv_popular (
                id INT PRIMARY KEY,
                title VARCHAR(255),
                vote_average FLOAT,
                popularity FLOAT,
                release_date DATE,
                type VARCHAR(10)
            )
        """)

        cursor.execute("""
            CREATE TABLE combined_popular (
                id INT PRIMARY KEY,
                title VARCHAR(255),
                vote_average FLOAT,
                popularity FLOAT,
                release_date DATE,
                type VARCHAR(10)
            )
        """)

        df_movies_popular = pd.read_csv("popular_movies.csv").dropna(subset=["id", "title", "vote_average", "popularity", "release_date", "type"])
        for _, row in df_movies_popular.iterrows():
            cursor.execute("""
                INSERT IGNORE INTO movies_popular (id, title, vote_average, popularity, release_date, type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                int(row["id"]),
                row["title"],
                row["vote_average"],
                row["popularity"],
                row["release_date"],
                row["type"]
            ))

        df_tv_popular = pd.read_csv("popular_series.csv").dropna(subset=["id", "title", "vote_average", "popularity", "release_date", "type"])
        for _, row in df_tv_popular.iterrows():
            cursor.execute("""
                INSERT IGNORE INTO tv_popular (id, title, vote_average, popularity, release_date, type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                int(row["id"]),
                row["title"],
                row["vote_average"],
                row["popularity"],
                row["release_date"],
                row["type"]
            ))

        df_combined = pd.concat([df_movies_popular, df_tv_popular], ignore_index=True)
        df_combined = df_combined.drop_duplicates(subset="id")
        df_combined = df_combined.sort_values(by="popularity", ascending=False)

        for _, row in df_combined.iterrows():
            cursor.execute("""
                INSERT IGNORE INTO combined_popular (id, title, vote_average, popularity, release_date, type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                int(row["id"]),
                row["title"],
                row["vote_average"],
                row["popularity"],
                row["release_date"],
                row["type"]
            ))

        conn.commit()
        conn.close()
        messagebox.showinfo("Base de Datos OK", "Base de datos creada y tablas llenadas correctamente.")
    except Exception as e:
        messagebox.showerror("Error BD", f"Error creando la base de datos:\n{e}")

root = Tk()
root.title("TMDB Scraper y Base de Datos")

# Activar pantalla completa
root.attributes('-fullscreen', True)

# Salir de pantalla completa con Escape
root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))

root.geometry("350x220")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use('clam')

titulo_font = font.Font(family="Helvetica", size=16, weight="bold")
btn_font = font.Font(family="Arial", size=12)

style.configure("My.TButton", font=btn_font)

frame = ttk.Frame(root, padding=20)
frame.pack(fill=BOTH, expand=True)

label_title = ttk.Label(frame, text="TMDB Scraper y Base de Datos", font=titulo_font, foreground="#2c3e50")
label_title.pack(pady=(0,20))

btn_scraping = ttk.Button(frame, text=" Hacer Web Scraping", command=hacer_scraping, style="My.TButton")
btn_scraping.pack(fill=X, pady=10)

btn_crear_bd = ttk.Button(frame, text=" Crear BD y Cargar Datos", command=crear_bd_y_cargar, style="My.TButton")
btn_crear_bd.pack(fill=X, pady=10)

root.mainloop()
