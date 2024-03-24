from bs4 import BeautifulSoup
import requests
import json
import time
from pprint import pprint


class GetData:
    @staticmethod
    def take_rss_data():
        articles_json = []
        r = requests.get('https://lenta.ru/rss/news')
        soup = BeautifulSoup(r.content, features='lxml')
        articles = soup.find_all('item')
        for a in articles:
            title = a.find('title').text
            category = a.find('category').text
            published = a.find('pubdate').text
            article = {
                'title': title,
                'category': category,
                'date': published
                }
            articles_json.append(article)
        return articles_json



class Logging:
    @staticmethod
    def save_function(article_list) -> None:
        with open('articles.json', 'w') as outfile:
            for i in article_list:
                json.dump(i, outfile,indent=2, ensure_ascii=False)

class Program:
    def __init__(self) -> None:
        self.get_data = GetData()
        self.logger = Logging()
    def display(self) -> None:
        data = self.get_data.take_rss_data()
        self.logger.save_function(data)
        for i in data:
            pprint(i)
    

if __name__ == '__main__':
    while True:
        app = Program()
        app.display()
        print('Scraping again in 5 minutes')
        print('Finished scraping')
        print('Saved to file')
        time.sleep(5)
      