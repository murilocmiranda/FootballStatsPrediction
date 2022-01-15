# https://www.soccerstats.com/results.asp?league=brazil_2020&pmtype=round1
import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup

def get_table(round, url, season_year):
    round_url = f'{url}/{round}'
    page = requests.get(round_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Parse HTML
    table = soup.find('table', id='btable')
    col_rows = table.findAll('tr', {'class': 'odd'})

    # Build data rows
    rows = []
    for child in col_rows:
        row = []
        row.append(str(season_year))
        for td in child:
            try:
                row.append(td.text.replace('\n', ''))
            except:
                continue
        if len(row) > 0:
            rows.append(row)

    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df


# Import
leagues = ['brazil']
season = ['2017', '2018', '2019', '2020', ''] # Empty is the current one
for league in leagues:
    for season in season:

        if (len(season) == 0):
            tmp_league_season = f'{league}'
            tmp_season_number = f'{datetime.datetime.now().year}'
        else:
            tmp_league_season = f'{league}_{season}'
            tmp_season_number = f'{season}'

        for round in range(1, 39, 1):
            print("-> %s - %s " % (tmp_league_season, round))

            name = 'https://www.soccerstats.com/'
            location = f'results.asp?league={tmp_league_season}&pmtype=round{round}'

            table = get_table(location, name, tmp_season_number)
            table.columns =['Year', 'Date', 'Home', 'Score', 'Away', 'Stats', 'Half-time score', 'Match total goals is over 2.5', 'Match total goals', 'Both teams scored']

            writer = pd.ExcelWriter(f'data/{tmp_league_season}-round-{round}.xlsx', engine='xlsxwriter')
            table.to_excel(writer, sheet_name='Games', index=False)
            writer.save()
