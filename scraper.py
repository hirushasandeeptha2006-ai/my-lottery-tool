import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_nlb_results():
    # NLB සයිට් එකේ results පිටුව
    url = "https://www.nlb.lk/english/results/"
    # Browser එකක් වගේ පෙන්නන්න header එකක් අනිවාර්යයෙන්ම ඕනේ
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        results_list = []
        
        # අලුත්ම සයිට් එකේ structure එකට අනුව දත්ත ගැනීම
        # 'result-block' කියන class එක තියෙන හැම එකක්ම බලනවා
        items = soup.find_all('div', class_='result-block')
        
        for item in items:
            name_tag = item.find('h3')
            if name_tag:
                name = name_tag.text.strip()
                # අංක තියෙන spans ටික ගන්නවා
                numbers = [n.text.strip() for n in item.find_all('span', class_='num-node') if n.text.strip()]
                
                if name and numbers:
                    results_list.append({
                        "name": name,
                        "numbers": numbers,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
        
        # JSON file එකට ලියනවා
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results_list, f, indent=4, ensure_ascii=False)
            
        print(f"Success! Found {len(results_list)} results.")

    except Exception as e:
        print(f"Error logic: {e}")

if __name__ == "__main__":
    get_nlb_results()
