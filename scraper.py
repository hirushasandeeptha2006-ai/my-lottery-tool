import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_nlb_results():
    # NLB English Results page
    url = "https://www.nlb.lk/english/results/"
    headers = {'User-Agent': 'Mozilla/5.0'} # Browser එකක් වගේ පෙන්නන්න
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        results_list = []
        
        # සයිට් එකේ අලුත්ම structure එකට අනුව දත්ත ගැනීම
        # අපි බලන්නේ හැම lottery block එකක්ම
        blocks = soup.find_all('div', class_='result-block')
        
        for block in blocks:
            name_tag = block.find('h3', class_='result-title')
            if name_tag:
                name = name_tag.text.strip()
                # අංක තියෙන span ටික හොයනවා
                num_nodes = block.find_all('span', class_='num-node')
                numbers = [n.text.strip() for n in num_nodes if n.text.strip()]
                
                if numbers: # අංක තියෙනවා නම් විතරක් එකතු කරගන්න
                    results_list.append({
                        "name": name,
                        "numbers": numbers,
                        "date": datetime.now().strftime("%Y-%m-%d")
                    })
        
        # දත්ත JSON file එකට ලියනවා
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results_list, f, indent=4, ensure_ascii=False)
            
        print(f"Success! {len(results_list)} lotteries found and saved.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_nlb_results()
