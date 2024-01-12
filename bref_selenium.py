from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_team_stats(team_code, season):
    driver_path = 'YOUR_PATH_HERE' 
    options = Options()
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) # Disables images -> faster runtime

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    url = f"https://www.basketball-reference.com/teams/{team_code}/{season}.html"
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    try:
        drtg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td[data-stat="def_rtg"]'))).text
        pace = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td[data-stat="pace"]'))).text
        return drtg, pace
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, None
    finally:
        driver.quit()

team_codes = [
    'ATL', 'BOS', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 
    'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'BRK', 
    'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS'
]

# Testing for just one team
team_code = 'ATL' 
season = '2024'
drtg, pace = scrape_team_stats(team_code, season)
print(f"{team_code} {season} - Defensive Rating: {drtg}, Pace: {pace}")
