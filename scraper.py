import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_nlb_results():
    url = "https://www.nlb.lk/english/results/"
    # Browser එකකින් එනවා වගේ පෙන්නන්න header එකක් දානවා
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results_list = []
        
        # සයිට් එකේ හැම result block එකක්ම පීරනවා
        blocks = soup.select('.result-block') 
        
        if not blocks:
            # වෙනත් විදියකට උත්සාහ කරමු
            blocks = soup.find_all('div', {'class': 'result-block'})

        for block in blocks:
            try:
                # ලොතරැයි නම
                name = block.find('h3').text.strip()
                
                # දිනුම් අංක සහ අකුරු
                # span එකේ තියෙන හැම අකුරක්/අංකයක්ම ගන්නවා
                numbers = [n.text.strip() for n in block.find_all('span') if n.text.strip()]
                
                # date එක සයිට් එකෙන්ම ගන්න උත්සාහ කරනවා, නැත්නම් අද දිනය දානවා
                date_tag = block.find('p', class_='result-date')
                date_val = date_tag.text.strip() if date_tag else datetime.now().strftime("%Y-%m-%d")

                if name and numbers:
                    results_list.append({
                        "name": name,
                        "numbers": numbers,
                        "date": date_val
                    })
            except Exception as e:
                continue
        
        # JSON එකට save කරනවා
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results_list, f, indent=4, ensure_ascii=False)
            
        print(f"සාර්ථකයි! ලොතරැයි {len(results_list)}ක් හමු වුණා.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_nlb_results()
