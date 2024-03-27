from bs4 import BeautifulSoup
import httpx
import json
from json import JSONDecodeError
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
        self.json_list = data
        self.json_file = 'data.json'

    def log_to_json_file(self) -> None:
        with open(self.json_file, "a") as json_file:
            for data in self.json_list:
                if not self._find_duplicate(data, 'title'):
                    json.dump(data, json_file,
                              indent=4, ensure_ascii=False)

    def _find_duplicate(self, item: dict, field: str) -> bool:
        try:
            with open(f"{self.json_file}", "r") as json_file:
                data = json.load(json_file)

                for chunk in data:
                    if chunk['title'] == item[field]:
                        return True
                return False
        except JSONDecodeError as error:
            print(f"Error: {error}")


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
