import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.basketball-reference.com/players/j/jamesle01/gamelog/2024' # can be any player game log from a specific season
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')  
    table = soup.find('table', {'id': 'pgl_basic'})
    headers = [th.text.strip() for th in table.find('thead').find_all('th') if th.get('data-stat')]
    rows = table.find('tbody').find_all('tr')
    data = []
    for row in rows:
        if row.get('class') is None or 'thead' not in row.get('class'):
            game_data = []
            for td in row.find_all('td'):
                game_data.append(td.text.strip())
            if row.find('td', {"data-stat": "game_location"}).text.strip() == '@':
                game_data.append('Away')
            else:
                game_data.append('Home')
            data.append(game_data)

    df = pd.DataFrame(data, columns=headers[1:] + ['Home/Away'])
    df.index += 1
    print(df[['Date', 'Opp', 'Home/Away', 'PTS']].head(10))  # Print first 10 rows
else:
    print("Failed to retrieve the webpage")
