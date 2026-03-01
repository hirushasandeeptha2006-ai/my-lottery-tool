import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_nlb_results():
    # NLB English results page
    url = "https://www.nlb.lk/english/results/"
    
    # මේ header එකෙන් GitHub එක real browser එකක් වගේ සයිට් එකට පේනවා
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        results_list = []
        
        # සයිට් එකේ අලුත්ම layout එකට අනුව data හොයනවා
        blocks = soup.find_all('div', class_='result-block')
        
        for block in blocks:
            try:
                name_el = block.find('h3', class_='result-title')
                if not name_el: continue
                
                name = name_el.text.strip()
                # අංක තියෙන span ටික ගන්නවා
                numbers = [span.text.strip() for span in block.find_all('span', class_='num-node') if span.text.strip()]
                
                if name and numbers:
                    results_list.append({
                        "name": name,
                        "numbers": numbers,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
            except:
                continue
        
        # දත්ත JSON එකට ලියනවා
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results_list, f, indent=4, ensure_ascii=False)
            
        print(f"Success: Found {len(results_list)} lotteries!") # මේක ලොග් එකේ පේනවා

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    get_nlb_results()
