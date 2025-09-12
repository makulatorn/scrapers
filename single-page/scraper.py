from bs4 import BeautifulSoup
import requests
import json

url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
response = requests.get(url)
html_data = response.content
soup = BeautifulSoup(html_data, "html.parser")

products = soup.find_all("div", class_="product-wrapper card-body")

product_list = []

for product in products:
    titles = product.find("a", class_="title")
    prices = product.find("span", itemprop="price")
    description = product.find("p", class_="description card-text")
    reviews = product.find("p", class_="review-count float-end")

    product.list.append(
        {
            "title": titles.text.strip(),
            "price": prices.text.strip(),
            "description": description.text.strip(),
            "reviews": reviews.text.strip(),
        }
    )

final_data = {"products": product_list}

with open("data.json", "w") as final:
    json.dump(product_list, final, indent=4)
