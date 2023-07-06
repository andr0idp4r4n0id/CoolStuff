import queue
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By

threads = []
q = queue.Queue()

def do_work(url):
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(options=options)
    editions = []
    driver.get(url)
    name = driver.find_element(By.CSS_SELECTOR, ".RuleDetailsstyles__StyledHeader-sc-q5wdmb-5 > h1:nth-child(1)").text.strip("\n")
    for edition in driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/nav/main/div/ul/div/li/a"):
        edition = edition.get_attribute("href").strip("\n")
        editions.append(edition)
    rule = url.split("/")[4].strip("\n")
    language = url.split("/")[3].strip("\n")
    print(f"{editions} \ {language}/{rule} \ {name} ", flush=True)
    driver.close()

def main(do_work):
    while True:
        try:
            url = q.get(timeout=3)
            do_work(url)
        except Exception as e:
            print(f"Failed: {url} {e}", flush=True)
        time.sleep(1)
        q.task_done()

with open("done.failed") as f:
    for url in f:
        q.put_nowait(url)
    for _ in range(3):
        threading.Thread(target=main, args=(do_work, ), daemon=True).start()
    q.join()