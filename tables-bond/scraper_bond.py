import pandas as pd
import requests
from io import StringIO

url = "https://en.wikipedia.org/wiki/List_of_James_Bond_films"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

bond_tables = pd.read_html(StringIO(response.text))

bond_data = bond_tables[0].convert_dtypes()

new_column_names = {
    ("Title", "Title"): "title",
    ("Year", "Year"): "year",
    ("Bond actor", "Bond actor"): "bond_actor",
    ("Director", "Director"): "director",
    ("Box office (millions)[15][16]", "Actual $"): "income_usa_actual",
    ("Box office (millions)[15][16]", "Adjusted $ (2024)"): "income_usa_adjusted",
    ("Budget (millions)[15][16]", "Actual $"): "budget_actual",
    ("Budget (millions)[15][16]", "Adjusted $ (2024)"): "budget_adjusted",
}

bond_data = bond_data.drop(columns=[("Ref(s)", "Ref(s)")])
bond_data.columns = [new_column_names.get(col, col) for col in bond_data.columns]
bond_data = bond_data[~bond_data["title"].str.contains("Eon", case=False, na=False)]

data = bond_data.assign(
    income_usa_actual=lambda data: pd.to_numeric(
        data["income_usa_actual"].replace("[$,]", "", regex=True), errors="coerce"
    ),
    budget_actual=lambda data: pd.to_numeric(
        data["budget_actual"].replace("[$,]", "", regex=True), errors="coerce"
    ),
    budget_adjusted=lambda data: pd.to_numeric(
        data["budget_actual"].replace("[$,]", "", regex=True), errors="coerce"
    ),
    year=lambda data: pd.to_numeric(data["year"], errors="coerce"),
).drop_duplicates(ignore_index=False)


data.columns = [
    col if isinstance(col, str) else new_column_names.get(col, f"{col[0]}_{col[1]}")
    for col in data.columns
]
data.loc[data.duplicated(keep=False)]
print(data)
