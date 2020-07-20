'''
THIS IS FOR SCRAPING THE LIST OF PRODUCTS

'''
import requests
from bs4 import BeautifulSoup
import json


class ProductScraping():
    url = "https://apps.shopify.com/browse/all?page="
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}

    def __init__(self, OUTPUT="products.json"):
        self.OUTPUT_FILE = OUTPUT
        with open(OUTPUT, 'w', encoding="utf-8") as f:
            details = {'product_links': []}
            json.dump(details, f, indent=2, ensure_ascii=False)

    def get_total_page_number(self):
        response = requests.get(self.url+'1')
        soup = BeautifulSoup(response.content, 'lxml')
        total_number = soup.find(
            'div', class_='grid__item grid__item--tablet-up-half').text
        number_splits = total_number.split()
        index_of = number_splits.index('of')
        number_in_page = number_splits[index_of - 1]
        total_number = number_splits[index_of+1]
        return int(number_in_page), int(total_number)

    def get_reponse(self, page_number):
        url = self.url + str(page_number)
        response = requests.get(url=url, headers=self.headers)
        if response.ok:
            return response
        else:
            print("Error is raised in url:: ", url)
            return None

    def get_all_products(self, response):
        """Getting the respone

        """
        soup = BeautifulSoup(response.content, 'lxml')
        list_of_product_links = soup.findAll('div', class_="ui-app-card")

        list_of_product = [link['data-target-href']
                           for link in list_of_product_links]

        return list_of_product

    def get_json_file(self, list_products):
        with open(self.OUTPUT_FILE, 'r+', encoding='utf-8') as f:
            load_json_file = json.load(f)
            load_json_file['product_links'].append(list_products)

            f.seek(0)
            f.write(json.dumps(
                load_json_file, indent=2, ensure_ascii=False))
            f.truncate()

    def start(self):
        number_in_page, total_page_number = self.get_total_page_number()
        total_pages = total_page_number//number_in_page
        for i in range(1, total_pages):
            print("Downloading the first page:::", i)
            response = self.get_reponse(i)
            if response:
                list_of_products = self.get_all_products(response)
                self.get_json_file(list_of_products)

            else:
                print("Not found!")


if __name__ == "__main__":
    bot = ProductScraping()
    bot.start()
