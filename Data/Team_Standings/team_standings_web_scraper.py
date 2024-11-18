from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

# Creating storage directory
os.mkdir("Data/Team_Standings/Expanded_Standings")

year = 2024

# Loop through all the years down to 2000
while year > 1999:
    # Skip over 2021 and 2020 (COVID affected years that need some treatment beforebeing converted into CSV)
    if year == 2020 or year == 2021:
        year -= 1
    else:
        # create URL
        url = f"https://www.basketball-reference.com/leagues/NBA_{year}_standings.html"

        # Load the dynamic tables on the page
        driver = webdriver.Chrome()

        driver.get(url)

        driver.implicitly_wait(100)

        page = driver.page_source

        soup = BeautifulSoup(page, "html.parser")

        # Get the table onject
        table = soup.findAll("table", id="expanded_standings", limit=1)[0]

        # Get the headeres for the data frame
        headers = table.find_all("th")
        header_list = []

        for header in headers:
            header_list.append(header.text)

        table_headers_start = header_list.index("Rk")
        table_headers_end = header_list.index("Apr") + 1

        table_headers = header_list[table_headers_start:table_headers_end]

        # Create the data frame with the given columns
        df = pd.DataFrame(columns=table_headers)

        column_data = table.findAll("tr")

        rank_start = header_list.index("1")

        ranks = header_list[rank_start:]

        i = 0

        for column in column_data:
            cells = column.find_all("td")

            individual_column_data = [cell.text.strip() for cell in cells]

            if individual_column_data == []:
                continue

            individual_column_data.insert(0, ranks[i])
            length = len(df)

            df.loc[length] = individual_column_data
            i += 1

        df.to_csv(f"Data/Team_Standings/Expanded_Standings/{year}.csv")
        year -= 1
