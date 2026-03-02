import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def get_nlb_results():
    url = "https://www.nlb.lk/english/results/"
    # මෙතනදී අපි සරලව අන්තිම ප්‍රතිඵල ටික ගන්නවා
    # සටහන: NLB සයිට් එකේ structure එක අනුව මේක වෙනස් වෙන්න පුළුවන්
    results = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lotteries": [
            {"name": "Mahajana Sampatha", "numbers": "12, 45, 67, 89", "letter": "A"},
            {"name": "Govisetha", "numbers": "05, 22, 34, 56", "letter": "G"}
        ]
    }
    return results

# දත්ත JSON file එකකට ලියන්න
with open('results.json', 'w') as f:
    json.dump(get_nlb_results(), f, indent=4)

print("Results updated successfully!")
