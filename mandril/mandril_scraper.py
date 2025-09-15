import pandas as pd
import requests
from io import StringIO

url = "https://da.wikipedia.org/wiki/Figurer_fra_Casper_%26_Mandrilaftalen"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

mandril_tables = pd.read_html(StringIO(response.text))
mandril_data = mandril_tables[1].convert_dtypes()

print(mandril_data)
