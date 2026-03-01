import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_nlb_results():
    url = "https://www.nlb.lk/english/results/"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results_list = []
        
        # ලොතරැයි නම සහ අංක ටික එකතු කරගන්නවා
        lotteries = soup.find_all('div', class_='result-block') # සයිට් එකේ block එක
        
        for item in lotteries[:10]: # අලුත්ම ලොතරැයි 10ක් ගමු
            name = item.find('h3', class_='result-title').text.strip()
            # අංක ටික එකතු කරගමු
            numbers = [n.text for n in item.find_all('span', class_='num-node')]
            
            results_list.append({
                "name": name,
                "numbers": numbers,
                "date": datetime.now().strftime("%Y-%m-%d")
            })
        
        # JSON file එකක් විදියට save කරනවා
        with open('results.json', 'w') as f:
            json.dump(results_list, f, indent=4)
            
        print("Success! 'results.json' file එක හැදුනා මචං.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_nlb_results()