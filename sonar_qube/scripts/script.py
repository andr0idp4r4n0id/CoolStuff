from selenium import webdriver
from selenium.webdriver.common.by import By

def main():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    hrefs = []
    editions = []
    with open("keys.txt") as f:
        for language in f:
            driver.get(f"https://rules.sonarsource.com/{language}")
            elem = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/nav/ol/li/a")
            for ele in elem:
                print(ele.get_attribute("href"))


main()