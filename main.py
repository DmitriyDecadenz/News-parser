from bs4 import BeautifulSoup
import httpx
import json
import time
from pprint import pprint


class GetData:
    def __init__(self) -> None:
        self.raw_data = []
        self.url = 'https://lenta.ru/rss/news'
        self.data_list = []

    def _take_rss_data(self) -> list:
        for i in range(3):
            try:
                r = httpx.get(self.url)
                break
            except:
                print("Error")
                time.sleep(3)
                continue

        soup = BeautifulSoup(r.content, features="lxml")
        self.raw_data = soup.find_all("item")
        return self.raw_data

    def pars_data(self) -> list:
        for a in self._take_rss_data():
            title = a.find("title").text
            category = a.find("category").text
            published = a.find("pubdate").text
            article = {"title": title, "category": category, "date": published}
            self.data_list.append(article)
        return self.data_list


class Logging:
    def __init__(self, data: list) -> None:
        self.data_list = data

    def log_to_json_file(self) -> None:
        with open("data.json", "w") as outfile:
            json.dump(self.data_list, outfile, indent=2, ensure_ascii=False)


class Program:

    def __init__(self) -> None:
        self.get_data = GetData()
        self.logger = Logging(self.get_data.pars_data())

    def display(self) -> None:

        for i in self.get_data.pars_data():
            pprint(i)
        self.logger.log_to_json_file()


if __name__ == "__main__":
    while True:
        app = Program()
        app.display()
        print("Finished scraping")
        print("Next scraping in 5 minutes")
        time.sleep(300)
