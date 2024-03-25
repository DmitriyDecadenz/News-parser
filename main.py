from bs4 import BeautifulSoup
import requests
import json
import time
from pprint import pprint


class GetData:
    def __init__(self) -> None:
        self.articles = []
        self.url = 'https://lenta.ru/rss/news'

    def take_rss_data(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, features="lxml")
        self.articles = soup.find_all("item")
        return self.articles


class ParsData:
    def __init__(self) -> None:
        self.data = GetData()
        self.data_list = []

    def pars_data(self):
        for a in self.data.take_rss_data():
            title = a.find("title").text
            category = a.find("category").text
            published = a.find("pubdate").text
            article = {"title": title, "category": category, "date": published}
            self.data_list.append(article)
        return self.data_list


class Logging:

    @staticmethod
    def save_function(data_list) -> None:
        with open("data.json", "w") as outfile:
            for i in data_list:
                json.dump(i, outfile, indent=2, ensure_ascii=False)


class Program:

    def __init__(self) -> None:
        self.get_data = ParsData()
        self.logger = Logging()

    def display(self) -> None:
        data = self.get_data.pars_data()
        self.logger.save_function(data)
        for i in data:
            pprint(i)


if __name__ == "__main__":
    while True:
        app = Program()
        app.display()
        print("Scraping again in 5 minutes")
        print("Finished scraping")
        print("Saved to file")
        time.sleep(5)