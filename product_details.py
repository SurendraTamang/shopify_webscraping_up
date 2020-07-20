"""
This module is for downloading the details

"""

import requests
from lxml import html
import time
import json


def get_details_of_product(url):
    reponse = requests.get(url)
    print("Getting the link ::", url)
    html_page = html.fromstring(reponse.content)
    categories_list = html_page.xpath(
        "//div[contains(@class,'heading--5')]/a/text()")
    app_name = html_page.xpath(
        "//h2[contains(@class,'ui-app-store-hero__header__app-name')]/text()")
    app_page = reponse.url
    website_link = html_page.xpath(
        "//a[contains(@class,'ui-external-link') and contains(text(),'website')]/@href")
    # Finding email
    span_finder = html_page.xpath("//span/text()")
    email = [email for email in span_finder if '@' in email]
    short_description = html_page.xpath(
        "//p[@class='heading--3 ui-app-store-hero__description']/text()")
    full_description = ' '.join(html_page.xpath(
        "//div[contains(@class,'app-listing__detailed-description')]//text()"))
    reviews = html_page.xpath(
        "//ul[contains(@class,'reviews-summary__rating-list')]/li")
    count = html_page.xpath("//a[contains(@href,'/reviews')]/text()")
    print(count)
    rating = html_page.xpath(
        "//span[contains(@class,'ui-star-rating__rating')]/text()")[0]
    pricing_model = html_page.xpath('//div[@class="pricing-plan-card__title"]')
    pricing = dict()
    for price in pricing_model:
        try:
            model = price.xpath("./h5/text()")[0].strip()

        except:
            model = "price"

        price_ = price.xpath("./h3/text()")[0].strip()

        pricing[model] = price_
    product_details = {
        "categories": categories_list,
        "app_name": app_name[0],
        "app_page": app_page,
        "website": website_link,
        "email": email[0],
        "short_description": short_description[0],
        "long_description": full_description.replace('\n', '').strip(),

        "reviews": {

            "count": int(count[-2].split()[2]),
            "5": remove_unwanted(html_page.xpath("//a[contains(@href,'?rating=5')]/text()")),
            "4": remove_unwanted(html_page.xpath("//a[contains(@href,'?rating=4')]/text()")),
            "3": remove_unwanted(html_page.xpath("//a[contains(@href,'?rating=3')]/text()")),
            "2": remove_unwanted(html_page.xpath("//a[contains(@href,'?rating=2')]/text()")),
            "1": remove_unwanted(html_page.xpath("//a[contains(@href,'?rating=1')]/text()"))
        },
        "rating": rating,
        "pricing":	pricing
    }
    dump_json_file(OUTPUT, product_details)


def remove_unwanted(sting):
    if sting:
        formated = sting[0]
        formated = formated.replace('(', '').replace(')', '')
        return int(formated)
    else:
        return None


def dump_json_file(OUTPUT, updated_data):
    print("Saving to json file::", updated_data['app_name'])
    with open(OUTPUT, 'r+', encoding="utf-8") as json_file:
        load_json_file = json.load(json_file)
        load_json_file['product_details'].append(updated_data)

        json_file.seek(0)
        json_file.write(json.dumps(
            load_json_file, indent=2, ensure_ascii=False))
        json_file.truncate()


if __name__ == "__main__":
    start = time.perf_counter()
    OUTPUT = "product_details.json"
    with open(OUTPUT, 'w', encoding="utf-8") as f:
        details = {'product_details': []}
        json.dump(details, f, indent=2, ensure_ascii=False)
    with open('products.json', 'r') as f:
        product_file = json.load(f)
        product_file = product_file['product_links']
        for batch_of_link in product_file:
            for url in batch_of_link:
                get_details_of_product(url
                                       )
