import requests
import pandas as pd
from tkinter import messagebox

API_KEY = "6e9456bdd4ec35e91f83f2cf2950e4c2"
BASE_URL = "https://api.themoviedb.org/3"

def fetch_tmdb_data(endpoint, pages=5):
    """Obtiene datos de la API de TMDB"""
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
    """Convierte los datos de la API a un DataFrame estructurado"""
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
    # Coordina todo el proceso de scraping
    popular_movies = fetch_tmdb_data("/movie/popular")
    top_rated_movies = fetch_tmdb_data("/movie/top_rated")
    popular_series = fetch_tmdb_data("/tv/popular")

    df_popular_movies = to_dataframe(popular_movies, "movie")
    df_top_rated_movies = to_dataframe(top_rated_movies, "movie")
    df_popular_series = to_dataframe(popular_series, "tv")

    df_popular_movies.to_csv("popular_movies.csv", index=False)
    df_top_rated_movies.to_csv("top_rated_movies.csv", index=False)
    df_popular_series.to_csv("popular_series.csv", index=False)

    return True
