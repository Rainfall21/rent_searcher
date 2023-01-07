from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSf_vLH-kBYiMcLyL9U-wAF93UY8-nBK8yVt0PpLP22JajyN8A/viewform?usp=sf_link"
# For ZILLOW variable go to zillow.com and choose your own parameters and copy and paste the link
ZILLOW = "https://www.zillow.com/new-york-ny/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.45346640039062%2C%22east%22%3A-73.50589559960937%2C%22south%22%3A40.41091408909013%2C%22north%22%3A40.9835584270191%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%7D"
ZILLOW_HOME = "https://www.zillow.com/"
CHROME_DRIVER_PATH = "/Users/alibekismagulov/Downloads/chromedriver"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(ZILLOW, headers=header)
data = response.text
soup = BeautifulSoup(data, "html.parser")

links = []
for link in soup.find_all(class_="property-card-link"):
    if link.get("href") not in links:
        links.append(link.get("href"))

prices = []
for price in soup.find_all(attrs={"data-test" : "property-card-price"}):
    prices.append(price.getText().split("+")[0])

addresses = []
for address in soup.find_all(attrs={"data-test" : "property-card-addr"}):
    addresses.append(address.getText().split(" | ")[1])

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)

for i in range(len(links)):

    driver.get(GOOGLE_FORM)

    addr_field = driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field = driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field = driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_btn = driver.find_element("xpath", '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    addr_field.send_keys(addresses[i])
    price_field.send_keys(prices[i])
    link_field.send_keys(ZILLOW_HOME+links[i])

    submit_btn.click()

driver.quit()
