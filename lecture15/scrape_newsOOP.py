import requests
from bs4 import BeautifulSoup
import json
import time
import os

base_url = "https://banks.am/am/news/100" 
pages_number = 2
final_result = {}

class NewsScraper:
    def __init__(self,get_pages,get_content,send_request,save_to_json):
        self.get_pages = get_pages
        self.get_content = get_content
        self.send_request = send_request
        self.save_to_json = save_to_json

    def get_pages(self):
        for self.page_number in range(1,self.pages_number +1):
            if self.page_number not in final_result:
                final_result[self.page_number] = []

        self.pages_url = f"{self.base_url}?page={self.page_number}"
        print(f"Scraping data from page {self.page_number}...")
    print(final_result)
    
    def send_request(self):
        self.resp = requests.get(self.pages_url)
        self.soup = BeautifulSoup(self.resp.text, 'html.parser')
        self.news_content = requests.get(self.a_tag.attrs["href"])
        self.news_content_soup = BeautifulSoup(self.news_content.text, 'html.parser')
    
    def get_content(self):
        if "href" in self.a_tag.attrs and self.a_tag.attrs["href"].startswith("https://banks.am/am/news/fintech/"):
            self.content_text = self.news_content_soup.find('br')
            self.content_text =' '.join([br_tag.next_sibling.strip() for br_tag in self.content_text if br_tag.next_sibling and br_tag.next_sibling.strip()])

    def final_result(self):
        final_result[self.page_number].append({
        "url": self.a_tag.attrs["href"],
        "content": self.news_content_text.get_text().replace('\n', ''),
        "title": self.news_content_soup.title.text.strip().replace('\n', '')
})
        time.sleep(1)
        print(f"Scrapping completed for {self.page_number}")

    def save_to_json(self):
        with open('news_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(final_result, json_file, ensure_ascii=False, indent=4)
        
        return final_result
    

scraper = NewsScraper(NewsScraper.get_pages, NewsScraper.send_request, NewsScraper.get_content, NewsScraper.save_to_json)
scraper.get_pages()
scraper.save_to_json()