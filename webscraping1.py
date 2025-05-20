import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import os  # Para crear directorio si no existe


def web_scrapping1():
    try:
        # Configuración del navegador
        driver_path = ChromeDriverManager().install()
        s = Service(driver_path)
        opc = Options()
        opc.add_argument('--window-size=1200,1200')
        browser = webdriver.Chrome(service=s, options=opc)
        browser.get('https://victoryroad.pro/sv-rental-teams/')
        time.sleep(3)  # Espera para cargar la página

        # Estructura para almacenar los datos
        teams_data = {
            'event': [],
            'best_result': [],
            'date': [],
            'pokemon_team': []
        }

        soup = BeautifulSoup(browser.page_source, 'html.parser')

        # Buscar la tabla (usamos select_one para obtener la primera tabla)
        tabla = soup.select_one("table.infobox2.sortable")

        if not tabla:
            print("No se encontró la tabla")
            return

        team_containers = tabla.find_all('tr')

        for container in team_containers[1:]:  # Saltar el encabezado
            celdas = container.find_all("td")

            print(celdas[2].text.split(','))
            # Extraer nombre del evento (primer <td>)
            event = celdas[2].find('a') if len(celdas) > 0 else None
            teams_data['event'].append(event.text.strip() if event else 'No event data')

            # Extraer mejor resultado (segundo <td>)
            best_result = celdas[2].get_text(strip=True) if len(celdas) > 1 else 'No result'
            teams_data['best_result'].append(best_result)

            # Extraer fecha (tercer <td>)
            date = celdas[2].get_text(strip=True) if len(celdas) > 2 else 'No date'
            teams_data['date'].append(date.strip('()'))  # Eliminar paréntesis

            # Extraer equipo Pokémon (cuarto <td>)
            pokemon_names = []
            if len(celdas) > 3:
                for img in celdas[3].find_all('img'):
                    name = img.get('title', '').strip()
                    if name:
                        pokemon_names.append(name)
            teams_data['pokemon_team'].append(pokemon_names)

        # Crear directorio si no existe
        os.makedirs('dataset', exist_ok=True)

        # Crear DataFrame y guardar CSV
        df = pd.DataFrame(teams_data)
        # print(df)
        df.to_csv('dataset/project_teams.csv', index=False)

    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
    finally:
        browser.quit()  # Asegura que el navegador se cierre siempre


if __name__ == '__main__':
    web_scrapping1()