from bs4 import BeautifulSoup
import os
import pandas as pd
import requests

year = 2000

while year < 2025:

    url = f"https://www.basketball-reference.com/awards/awards_{year}.html"

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    table = soup.findAll("table", limit=1)[0]

    headers = table.findAll("th")

    header_text = [header.text for header in headers]

    header_start = header_text.index("Rank")

    header_end = header_text.index("WS/48") + 1

    header_text = header_text[header_start:header_end]

    df = pd.DataFrame(columns=header_text)

    column_data = table.findAll("tr")

    for row in column_data:
        length = len(df)
        if length < 5:
            row_data = []
            for cell in row:
                row_data.append(cell.text.strip())
            if len(row_data) == 20:
                df.loc[length] = row_data

    df.to_csv(f"Data/MVP_Stats/Voting/{year}.csv")
    year += 1

print(df)
