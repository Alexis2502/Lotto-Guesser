import time
import requests
from bs4 import BeautifulSoup
from src.backend.lotto_database import save_sequences_to_db

def scrape_and_find_sequences_helper(content, game_type):
    soup = BeautifulSoup(content, 'html.parser')
    sequences = []

    numbers_in_list = soup.find_all('li', class_='numbers_in_list')
    current_sequence = []

    for number_li in numbers_in_list:
        number = number_li.get_text().strip()
        if number.isdigit():
            current_sequence.append(number)
            if len(current_sequence) == 6 and game_type == 'Lotto':
                sequences.append(current_sequence)
                current_sequence = []
            elif len(current_sequence) == 5 and (game_type == 'EuroJackpot' or game_type == 'MiniLotto'):
                sequences.append(current_sequence)
                current_sequence = []

    return sequences

def scrape_and_find_sequences(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            if 'eurojackpot' in url:
                game_type = 'EuroJackpot'
            elif 'mini-lotto' in url:
                game_type = 'MiniLotto'
            else:
                game_type = 'Lotto'

            sequences = scrape_and_find_sequences_helper(response.content, game_type)
            save_sequences_to_db(sequences, game_type)
            return sequences
        else:
            print(f"Błąd podczas pobierania strony {url}: {response.status_code}")
            return []
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania strony {url}: {str(e)}")
        return []