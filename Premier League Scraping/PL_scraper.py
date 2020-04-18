from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

with open('PL_scraped.csv', mode='w', encoding='utf-8') as file:
    file.write('season,match_week,date,kickoff,referee,stadium,attendance,home,away,home_score,away_score,'
               'home_ht_score,away_ht_score,home_goals,away_goals,home_yellow_pl,away_yellow_pl,'
               'home_red_pl,away_red_pl,home_posse,away_posse,home_shotsON,away_shotsON,home_shots,away_shots,'
               'home_passes,away_passes,home_corners,away_corners,home_offsides,away_offsides,'
               'home_yellows,away_yellows,home_reds,away_reds,home_fouls,away_fouls,home_lineup,away_lineup\n')

errors = 0
error_dict = {}

for i in range(46605, 46895):

    # Opening the connection and grabbing the page
    my_url = f'https://www.premierleague.com/match/{i}'
    option = Options()
    option.headless = True
    driver = webdriver.Chrome(options=option)
    driver.get(my_url)

    # Getting the season from the head
    title = driver.find_element_by_xpath('/html/head/title')
    title_html = title.get_attribute('outerHTML')

    # HTML parsing
    title_soup = BeautifulSoup(title_html, 'html.parser').text

    # Getting the data
    season_and_league = title_soup.split(',')[1]
    season = season_and_league.split('|')[0].strip()
    league = season_and_league.split('|')[1].strip()

    # Getting the match's data
    match_centre = driver.find_element_by_class_name('matchCentre')
    match_html = match_centre.get_attribute('outerHTML')

    try:
        # html parsing
        soup = BeautifulSoup(match_html, 'html.parser')

        # Getting the data
        match_week = soup.find('div', class_="short").text.replace('MW', '').strip()
        home = soup.find('div', class_='team home').a.find_next('span', class_='long').text.strip()
        away = soup.find('div', class_='team away').a.find_next('span', class_='long').text.strip()
        date = driver.find_element_by_xpath(
            "//div[@class='matchInfo']//div[@class='matchDate renderMatchDateContainer']").text
        ref = soup.find('div', class_='referee').text.strip()
        kickoff = driver.find_element_by_xpath("//strong[@class='renderKOContainer']").text
        stadium = soup.find('div', class_='stadium').text.replace(',', '-')
        att = soup.find('div', class_='attendance').text.replace(',', '')
        home_score = soup.find('div', class_="matchScoreContainer").text.strip()[0]
        away_score = soup.find('div', class_='matchScoreContainer').text.strip()[2]
        home_ht_score = soup.find('div', class_='halfTime').text.replace('HT:', '').replace('Half Time:', '').strip()[0]
        away_ht_score = soup.find('div', class_='halfTime').text.replace('HT:', '').replace('Half Time:', '').strip()[2]

        print(f'Scraping data from {home} vs {away}, matchweek {match_week}, season {season}...')

        teams = ['home', 'away']

        # Scraping goal scorers
        events = soup.find('div', class_='matchEventsContainer')
        goals = []
        for team in teams:
            team_events = events.find('div', class_=team)
            team_events_each = team_events.find_all('div', class_='event')
            team_goals = ''
            for event in team_events_each:
                type_event = event.find('span', class_='visuallyHidden').text
                if type_event == 'Red Card' or type_event == 'Second Yellow Card (Red Card)':
                    continue
                else:
                    team_goals += event.text.replace('Own Goal', '').replace('Goal', '').replace('label.penalty.scored',
                                                                                                 '').replace(',',
                                                                                                             ' ').strip() + ' - '
            goals.append(team_goals)

        # Scraping cards
        card_events = soup.find('div', class_='eventLine timeLineEventsContainer')
        yellow_cards = []
        red_cards = []
        for team in teams:
            team_card_events = card_events.find_all('div', class_=f'event {team}')
            team_yellow_cards = ''
            team_red_cards = ''
            card = ''
            for event in team_card_events:
                try:
                    card = event.find('span', class_='icn card-yellow').text
                except:
                    try:
                        card = event.find('span', class_='icn card-red').text
                    except:
                        try:
                            card = event.find('span', class_='icn card-yellowred').text
                        except:
                            continue
                if card == 'Yellow Card':
                    team_yellow_cards += event.find('a', class_='name').text.split('.')[1].strip() + ' - '
                if card == 'Red Card':
                    team_red_cards += event.find('a', class_='name').text.split('.')[1].strip() + ' - '
                if card == 'Second Yellow Card (Red Card)':
                    team_red_cards += event.find('a', class_='name').text.split('.')[1].strip() + ' - '
            yellow_cards.append(team_yellow_cards)
            red_cards.append(team_red_cards)

        # Scraping stats
        elem = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@class='tablist']//li[@data-tab-index='2']")))
        elem.click()
        sleep(5)
        dfs = pd.read_html(driver.page_source)

        for df in dfs:
            if len(df) > 3:
                if df.iloc[0, 1] == 'Possession %':
                    stats = df

        stats_check_home = ['home_possession_%', 'home_shots_on_target', 'home_shots', 'home_touches', 'home_passes',
                            'home_tackles', 'home_clearances', 'home_corners', 'home_offsides', 'home_yellow_cards',
                            'home_red_cards', 'home_fouls_conceded']
        stats_check_away = ['away_possession_%', 'away_shots_on_target', 'away_shots', 'away_touches', 'away_passes',
                            'away_tackles', 'away_clearances', 'away_corners', 'away_offsides', 'away_yellow_cards',
                            'away_red_cards', 'away_fouls_conceded']

        home_stats = {}
        away_stats = {}
        for team in teams:
            for i in range(len(stats)):
                name = team + ' ' + stats.iloc[i, 1]
                name = name.replace(' ', '_').lower()
                if team == 'home':
                    stat = stats.iloc[i, 0]
                    home_stats[name] = str(stat)
                else:
                    stat = stats.iloc[i, 2]
                    away_stats[name] = str(stat)

        for stat in stats_check_home:
            if stat not in home_stats.keys():
                home_stats[stat] = '0'

        for stat in stats_check_away:
            if stat not in away_stats.keys():
                away_stats[stat] = '0'

        # Scraping the line-ups
        lineups = {'home': '', 'away': ''}

        elem = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@class='tablist']//li[@data-tab-index='1']")))
        elem.click()
        sleep(5)

        lineup_home = driver.find_element_by_xpath(
            '//*[@id="mainContent"]/div/section/div[2]/div[2]/div[2]/section[2]/div/div/div[1]/div/div')
        lineup_home_html = lineup_home.get_attribute('outerHTML')
        lineup_home_soup = BeautifulSoup(lineup_home_html, 'html.parser')

        players_home = lineup_home_soup.find_all('span', class_='name')

        for player in players_home[:11]:
            player_name = player.text.split('Substitution Off')[0].strip().replace('Goal', '').replace('Yellow Card',
                                                                                                       '').replace(
                'Red Card', '').replace('Second  ()', '')
            lineups["home"] += player_name + ' - '

        lineup_away = driver.find_element_by_xpath(
            '//*[@id="mainContent"]/div/section/div[2]/div[2]/div[2]/section[2]/div/div/div[3]')
        lineup_away_html = lineup_away.get_attribute('outerHTML')
        lineup_away_soup = BeautifulSoup(lineup_away_html, 'html.parser')

        players_away = lineup_away_soup.find_all('span', class_='name')

        for player in players_away[:11]:
            player_name = player.text.split('Substitution Off')[0].strip().replace('Goal', '').replace('Yellow Card',
                                                                                                       '').replace(
                'Red Card', '').replace('Second  ()', '')
            lineups["away"] += player_name + ' - '

        driver.quit()

    except:
        print('\033[1;31mERROR!\033[m')
        errors += 1
        error_dict[errors] = {'Match Number': i, 'Season': season, 'Match Week': match_week,
                              'Home Team': home, 'Away Team': away}
        continue

    with open('PL_scraped.csv', mode='a', encoding='utf-8') as file:
        file.write(
            season + ',' + match_week + ',' + date + ',' + kickoff + ',' + ref + ',' + stadium + ',' + att + ',' +
            home + ',' + away + ',' + home_score + ',' + away_score + ',' + home_ht_score + ',' + away_ht_score + ',' +
            goals[0] + ',' + goals[1] + ',' + yellow_cards[0] + ',' + yellow_cards[1] + ',' +
            red_cards[0] + ',' + red_cards[1] + ',' + home_stats["home_possession_%"] + ',' +
            away_stats["away_possession_%"] + ',' + home_stats["home_shots_on_target"] + ',' +
            away_stats["away_shots_on_target"] + ',' + home_stats["home_shots"] + ',' + away_stats["away_shots"] + ',' +
            home_stats["home_passes"] + ',' + away_stats["away_passes"] + ',' + home_stats["home_corners"] + ',' +
            away_stats["away_corners"] + ',' + home_stats["home_offsides"] + ',' + away_stats["away_offsides"] + ',' +
            home_stats["home_yellow_cards"] + ',' + away_stats["away_yellow_cards"] + ',' +
            home_stats["home_red_cards"] + ',' + away_stats["away_red_cards"] + ',' +
            home_stats["home_fouls_conceded"] + ',' + away_stats["away_fouls_conceded"] + ',' +
            lineups["home"] + ',' + lineups["away"] + '\n')

    print('\033[1;34mDone!\033[m')

print('\nErrors: {}'.format(errors))
print(error_dict)
