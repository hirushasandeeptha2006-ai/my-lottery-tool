import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

def fetch_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_nlb():
    html = fetch_data("https://www.nlb.lk/english/results/")
    results = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        blocks = soup.select('.result-block')
        for b in blocks:
            try:
                name = b.find('h3').text.strip()
                nums = [s.text.strip() for s in b.find_all('span') if s.text.strip()]
                date = b.find('p', class_='result-date').text.strip() if b.find('p', class_='result-date') else datetime.now().strftime("%Y-%m-%d")
                if name and nums:
                    results.append({"name": name, "numbers": nums, "date": date, "source": "NLB"})
            except: continue
    return results

def scrape_dlb():
    # DLB data (පොදු දත්ත එකතු කිරීමක්)
    html = fetch_data("https://www.dlb.lk/english/results")
    results = []
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        # DLB සයිට් එකේ structure එක අනුව මෙතන වෙනස් විය හැක
        # දැනට අපි NLB එකට ප්‍රමුඛතාවය දෙමු, නමුත් DLB support එක මෙතනට එක් කළ හැක
        pass
    return results

def main():
    print("Scraping started...")
    all_results = scrape_nlb()
    
    if not all_results:
        print("දත්ත ලැබුණේ නැත! සයිට් එකේ structure එක වෙනස් වෙලා වගේ.")
    
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    
    print(f"Done! {len(all_results)} results saved to results.json")

if __name__ == "__main__":
    main()
