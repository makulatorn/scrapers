import pandas as pd
import requests

url = "https://en.wikipedia.org/wiki/List_of_James_Bond_novels_and_short_stories"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

bond_tables = pd.read_html(response.text)

bond_data = bond_tables[1].convert_dtypes()

print(bond_data)
