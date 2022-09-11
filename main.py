import requests
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

if __name__ == "__main__":

    result = [[], [], [], [], []]

    header = {"user-agent" : UserAgent().random}

    main_link = "https://health-diet.ru"

    link = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
    response = requests.get(link, headers=header).text
    soup = BeautifulSoup(response, "lxml")

    grid_content = soup.find("div", id="mzr-grid-content")
    block = grid_content.find("div", {"class" : "uk-grid uk-grid-medium"})
    links = block.find_all("a", {"class" : "mzr-tc-group-item-href"})

    for elem in links:

        item_link = f'{main_link}{elem.get("href")}'
        item_response = requests.get(item_link).text
        item_soup = BeautifulSoup(item_response, "lxml")

        table = item_soup.find("table")
        tbody = table.find("tbody")
        tr = tbody.find_all("tr")

        for item_block in tr:
            td = item_block.find_all("td")
            
            for i in range(len(td)):
                result[i].append(td[i].text.replace("\n", ""))

    df = pd.DataFrame({
        "Наименование" : result[0],
        "Калорийность" : result[1],
        "Белки" : result[2],
        "Жиры" : result[3],
        "Углеводы" : result[4]
    })

    df.to_excel("food_db.xlsx", index=False)