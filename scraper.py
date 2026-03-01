import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_nlb_results():
    url = "https://www.nlb.lk/english/results/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results_list = []
        
        # සයිට් එකේ හැම result block එකක්ම පීරලා බලනවා
        items = soup.find_all('div', class_='result-block')
        
        for item in items:
            try:
                name = item.find('h3').text.strip()
                # අංක සහ අකුරු ඔක්කොම ගන්නවා (span වල තියෙන)
                numbers = [n.text.strip() for n in item.find_all('span') if n.text.strip().isalnum()]
                date_str = datetime.now().strftime("%Y-%m-%d")

                if name and numbers:
                    results_list.append({
                        "name": name,
                        "numbers": numbers,
                        "date": date_str
                    })
            except:
                continue
        
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results_list, f, indent=4, ensure_ascii=False)
            
        print(f"වැඩේ ගොඩ! ලොතරැයි {len(results_list)} ක දත්ත ලැබුණා.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_nlb_results()
