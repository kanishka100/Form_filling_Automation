import requests
from bs4 import BeautifulSoup
import lxml
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url_to_form = 'https://forms.gle/nC6LMaX6JHsX4Kk3A'
driver = webdriver.Chrome(ChromeDriverManager().install())

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54 "
}
response = requests.get(
    'https://www.zillow.com/san-francisco-ca/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.61529005957031%2C%22east%22%3A-122.25136794042969%2C%22south%22%3A37.703343724016136%2C%22north%22%3A37.847169233586946%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A895865%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D',
    headers=headers)
zillow_page_html = response.text
links_list = []
soup = BeautifulSoup(zillow_page_html, 'html.parser')
links = soup.find_all(name="a", class_="list-card-link")
for l in links:
    links_list.append(l.get('href'))

addresses = [addr.text for addr in soup.find_all(name='address', class_='list-card-addr')]
price = [t.text for t in soup.find_all(name='div', class_='list-card-price')]

print(links_list)
print("\n", addresses)
print(price)
time.sleep(3)
driver.get(url_to_form)
time.sleep(3)


for k in range(3):

    address_feild = driver.find_elements_by_class_name('exportInput')
    address_feild[0].send_keys(addresses[k])
    address_feild[1].send_keys(price[k])
    address_feild[2].send_keys(links_list[k])
    button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
    button.click()
    time.sleep(3)
    next_form = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_form.click()
    time.sleep(3)

