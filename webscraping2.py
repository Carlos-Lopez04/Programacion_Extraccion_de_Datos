import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Importación faltante añadida
from bs4 import BeautifulSoup
import pandas as pd
import os


def setup_browser():
    """Configura el navegador Chrome de manera sencilla"""
    # Configura el servicio del navegador
    service = Service(ChromeDriverManager().install())

    # Opciones para el navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1200,1200')  # Tamaño de ventana
    options.add_argument('--disable-notifications')  # Desactiva notificaciones

    return webdriver.Chrome(service=service, options=options)


def search_pokemon(browser, name):
    """Busca un Pokémon en Pikalytics y devuelve el HTML"""
    try:
        # Ir a la página principal
        browser.get('https://www.pikalytics.com/')
        time.sleep(3)  # Esperar a que cargue

        # Localizar el campo de búsqueda
        search_box = browser.find_element(By.ID, 'search')
        search_box.clear()  # Limpiar por si acaso
        search_box.send_keys(name)
        time.sleep(2)  # Esperar a que aparezcan resultados

        # Intentar hacer click en el resultado específico
        try:
            result = browser.find_element(By.CSS_SELECTOR, f"a.pokedex_entry[data-name='{name}']")
            result.click()
            print(f"Click en el resultado para {name}")
        except:
            # Si no se encuentra el resultado, presionar Enter
            search_box.send_keys(Keys.ENTER)
            print(f"Usando ENTER para buscar {name}")

        time.sleep(5)  # Esperar a que cargue la página
        return BeautifulSoup(browser.page_source, 'html.parser')

    except Exception as e:
        print(f"Error al buscar {name}: {e}")
        return None


def get_pokemon_info(soup, pokemon_name):
    """Extrae toda la información del Pokémon de la página"""
    if not soup:
        return None

    # 1. Obtener tipos del Pokémon
    types = []
    type_spans = soup.select('span.pokedex-header-types span.type')
    if type_spans:
        types.append(type_spans[0].text.strip().lower())
        if len(type_spans) > 1:
            types.append(type_spans[1].text.strip().lower())

    # 2. Obtener estadísticas base
    stats = {}
    stat_divs = soup.find_all('div', style=lambda v: 'display:inline-block;width:30px;text-align: left;' in str(v))

    for div in stat_divs:
        stat_name = div.get_text(strip=True)
        value_div = div.find_next('div', style=lambda
            v: 'display:inline-block;vertical-align: middle;margin-left: 20px;' in str(v))
        if value_div:
            try:
                stats[stat_name] = int(value_div.get_text(strip=True))
            except:
                stats[stat_name] = None

    # 3. Obtener movimientos principales (máximo 3)
    moves = []
    move_entries = soup.find_all('div', class_='pokedex-move-entry-new')[:3]  # Limitar a 3 movimientos

    for move in move_entries:
        move_info = {
            'name': move.find('div', style='margin-left:10px;display:inline-block;').get_text(strip=True) if move.find(
                'div', style='margin-left:10px;display:inline-block;') else None,
            'type': move.find('span', class_='type').get_text(strip=True).lower() if move.find('span',
                                                                                               class_='type') else None,
            'usage': float(move.find('div', style='display:inline-block;float:right;').get_text(strip=True).replace('%',
                                                                                                                    '')) if move.find(
                'div', style='display:inline-block;float:right;') else None
        }
        if move_info['name']:
            moves.append(move_info)

    # 4. Obtener compañeros de equipo (máximo 3)
    teammates = []
    teammate_entries = soup.select('a.teammate_entry_pokedex-move-entry-new')[:3]  # Limitar a 3 compañeros

    for teammate in teammate_entries:
        teammate_info = {
            'name': teammate.find('span').get_text(strip=True) if teammate.find('span') else None,
            'type1': teammate.find_all('span', class_='type')[0].get_text(strip=True).lower() if teammate.find_all(
                'span', class_='type') else None,
            'type2': teammate.find_all('span', class_='type')[1].get_text(strip=True).lower() if len(
                teammate.find_all('span', class_='type')) > 1 else None,
            'usage': float(
                teammate.find('div', style='display:inline-block;float:right;').get_text(strip=True).replace('%',
                                                                                                             '')) if teammate.find(
                'div', style='display:inline-block;float:right;') else None
        }
        if teammate_info['name']:
            teammates.append(teammate_info)

    # Preparar datos finales
    pokemon_data = {
        'pokemon': pokemon_name.lower(),
        'primary_type': types[0] if len(types) > 0 else None,
        'secondary_type': types[1] if len(types) > 1 else None,
        'hp': stats.get('HP'),
        'attack': stats.get('Atk'),
        'defense': stats.get('Def'),
        'sp_attack': stats.get('SpA'),
        'sp_defense': stats.get('SpD'),
        'speed': stats.get('Spe'),
        'main_moves': moves,
        'common_teammates': teammates,
        'last_updated': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
    }

    return pokemon_data


def save_pokemon_data(data, filename='pokemon_stats.csv'):
    """Guarda los datos del Pokémon en un archivo CSV"""
    try:
        # Crear directorio si no existe
        os.makedirs('dataset', exist_ok=True)

        # Convertir los datos a DataFrame
        df = pd.DataFrame([data])

        # Si el archivo existe, cargarlo y añadir los nuevos datos
        filepath = f'pokemon_data/{filename}'
        if os.path.exists(filepath):
            existing_df = pd.read_csv(filepath)
            # Eliminar datos antiguos del mismo Pokémon si existen
            existing_df = existing_df[existing_df['pokemon'] != data['pokemon']]
            df = pd.concat([existing_df, df], ignore_index=True)

        # Guardar el DataFrame
        df.to_csv(filepath, index=False)
        print(f"Datos guardados en {filepath}")

    except Exception as e:
        print(f"Error al guardar datos: {e}")


def main():
    # Lista de Pokémon a analizar
    pokemon_to_analyze = ["raichu", "xerneas", "vaporeon"]  # Puedes modificar esta lista

    # Configurar el navegador
    browser = setup_browser()

    try:
        for pokemon in pokemon_to_analyze:
            print(f"\nObteniendo datos de {pokemon}...")

            # 1. Buscar el Pokémon y obtener el HTML
            soup = search_pokemon(browser, pokemon)

            if soup:
                # 2. Extraer la información del Pokémon
                pokemon_data = get_pokemon_info(soup, pokemon)

                if pokemon_data:
                    # 3. Mostrar resumen en consola
                    print(f"\nInformación de {pokemon}:")
                    print(f"Tipos: {pokemon_data['primary_type']}/{pokemon_data['secondary_type']}")
                    print(
                        f"Estadísticas - HP: {pokemon_data['hp']}, Ataque: {pokemon_data['attack']}, Defensa: {pokemon_data['defense']}")
                    print("Movimientos principales:")
                    for move in pokemon_data['main_moves']:
                        print(f"- {move['name']} ({move['type']}): {move['usage']}%")
                    print("Compañeros frecuentes:")
                    for teammate in pokemon_data['common_teammates']:
                        types = f"{teammate['type1']}/{teammate['type2']}" if teammate['type2'] else teammate['type1']
                        print(f"- {teammate['name']} ({types}): {teammate['usage']}%")

                    # 4. Guardar los datos
                    save_pokemon_data(pokemon_data)
                else:
                    print(f"No se pudo extraer información de {pokemon}")
            else:
                print(f"No se pudo cargar la página de {pokemon}")

            time.sleep(2)  # Espera entre búsquedas

    finally:
        # Cerrar el navegador al finalizar
        browser.quit()
        print("\nProceso completado. El navegador se ha cerrado.")


if __name__ == '__main__':
    main()