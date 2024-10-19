import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_40m_spots(driver):
    url = "https://www.reversebeacon.net/main.php?zoom=46.83,49.69,3.60&rows=100&max_age=20,minutes&bands=40&hide="

    driver.get(url)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#id_spots tr.spot.spots"))
        )

        time.sleep(2)

        html_content = driver.page_source
    except Exception as e:
        print(f"Error loading page: {e}")
        return []

    soup = BeautifulSoup(html_content, 'lxml')

    spot_table = soup.find('table', id='id_spots')

    if not spot_table:
        print("Could not find the spots table.")
        return []

    spots_data = []
    for row in spot_table.find_all('tr', class_='spot spots'):
        cells = row.find_all('td')
        if len(cells) >= 11:
            spot = {
                "dx": cells[0].text.strip(),
                "de": cells[1].text.strip(),
                "distance_mi": cells[2].text.strip(),
                "distance_km": cells[3].text.strip(),
                "freq": cells[4].text.strip(),
                "mode": cells[5].text.strip(),
                "type": cells[6].text.strip(),
                "db": cells[7].text.strip(),
                "speed": cells[8].text.strip(),
                "date": cells[9].text.strip(),
                "last_reported": cells[10].text.strip()
            }
            freq = float(spot['freq'])
            if 7000.0 <= freq <= 7300.0:
                spots_data.append(spot)

    return spots_data


def main():
    while True:
        print("Fetching new data...")
        driver = webdriver.Firefox()

        spots = get_40m_spots(driver)
        print(f"Found {len(spots)} spots in the 40m band.")
        print(spots)


        print("Waiting for 20 seconds before next update...")
        time.sleep(20)


if __name__ == "__main__":
    main()
