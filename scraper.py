import requests
import re
import json
from datetime import datetime

def get_lottery():
    # අපි පාවිච්චි කරන්නේ සරලම URL එක
    url = "https://www.nlb.lk/english/results/mahajana-sampatha" # උදාහරණයකට මහජන සම්පත ගමු
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    results_list = []
    
    # ලොතරැයි වර්ග කිහිපයක නම්
    lotteries = ['mahajana-sampatha', 'vasana-sampatha', 'govisetha', 'dhana-nidhanaya', 'mega-power']

    for lotto in lotteries:
        try:
            target_url = f"https://www.nlb.lk/english/results/{lotto}"
            response = requests.get(target_url, headers=headers, timeout=20)
            
            # HTML එක ඇතුළේ තියෙන අංක සොයන්න (Regex පාවිච්චි කරලා)
            # සාමාන්‍යයෙන් අංක තියෙන්නේ <span class="num-node"> ඇතුළේ
            numbers = re.findall(r'<span class="num-node">([^<]+)</span>', response.text)
            
            if numbers:
                results_list.append({
                    "name": lotto.replace('-', ' ').title(),
                    "numbers": numbers[:7], # මුල් අංක ටික විතරක් ගමු
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                print(f"Found {lotto}")
        except:
            continue

    # JSON එකට ලියනවා
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(results_list, f, indent=4)

if __name__ == "__main__":
    get_lottery()
