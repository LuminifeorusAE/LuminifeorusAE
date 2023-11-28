import requests
from bs4 import BeautifulSoup
import json
import time

url = "https://banks.am/am/news/100" 
pages = 2
final_result = {}
    
def scrape_news(url, pages):
    for page_number in range(1,pages +1):
        if page_number not in final_result:
            final_result[page_number] = []

        pages_url = f"{url}?page={page_number}"
        print(f"Scraping data from page {page_number}...")
        
        resp = requests.get(pages_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        get_links = soup.find_all("a")

        
        for a_tag in get_links:
            if "href" in a_tag.attrs and a_tag.attrs["href"].startswith("https://banks.am/am/news/fintech/"):
                news_content = requests.get(a_tag.attrs["href"])
                news_content_soup = BeautifulSoup(news_content.text, 'html.parser')
                news_content_text = news_content_soup.find_all("div", class_="news-text")[0]
                content_text = news_content_soup.find('br')
                content_text = ' '.join([br_tag.next_sibling.strip() for br_tag in content_text if br_tag.next_sibling and br_tag.next_sibling.strip()])


                final_result[page_number].append({
                "url": a_tag.attrs["href"],
                "content": news_content_text.get_text().replace('\n', ''),
                "title": news_content_soup.title.text.strip().replace('\n', '')
})

        time.sleep(1)
        print(f"Scrapping completed for {page_number}")

    with open('news_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(final_result, json_file, ensure_ascii=False, indent=4)
        
        return final_result
    
news_data = scrape_news(url, pages)
print(news_data)