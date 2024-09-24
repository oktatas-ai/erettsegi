from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import time
import re
import os

OKTATAS_HU = "https://www.oktatas.hu"

# Initialize the webdriver and dom element presence awaiter
driver = webdriver.Safari()
wait = WebDriverWait(driver, 60)

# Scrape every erettsegi pdf url from dari.oktatas.hu - only until 2020
pre_twenty_pdf_urls = set()
for verbose_subject in tqdm(["történelem", "magyar nyelv és irodalom", "matematika"]):
    driver.get("https://dari.oktatas.hu/erettsegi.utmutato.index")
    select = Select(
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main"]/section/div/div[3]/div/div[1]/div/select'),
            ),
        ),
    )
    select.select_by_visible_text(verbose_subject)
    table = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main"]/section/div/div[4]/table'),
        ),
    )
    soup = BeautifulSoup(table.get_attribute("outerHTML"), "html.parser")
    urls = list(link["href"] for link in soup.find_all("a", href=True))
    pre_twenty_pdf_urls.update(urls)

# Scrape every erettsegi url from oktatas.hu - available after 2020 till today
erettsegi_urls = set()
driver.get("https://www.oktatas.hu/kozneveles/erettsegi/feladatsorok")
table = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[@id="ohm_content"]/div[1]/table[2]'),
    ),
)
soup = BeautifulSoup(table.get_attribute("outerHTML"), "html.parser")
urls = list(link["href"] for link in soup.find_all("a", href=True))
erettsegi_urls.update(urls)

# Filter out post-twenty erettsegi urls
post_twenty_erettsegi_urls = set()
pattern = r"/kozneveles/erettsegi/feladatsorok/(\w+)_20(\d{2})(\w+)"
for url in tqdm(erettsegi_urls):
    if match := re.search(pattern, url):
        if int(match.group(2)) in range(20, time.localtime().tm_year % 100 + 1):
            post_twenty_erettsegi_urls.add(OKTATAS_HU + url)

# Scrape erettsegi day urls for post-twenty erettsegi urls
post_twenty_erettsegi_day_urls = set()
for url in tqdm(post_twenty_erettsegi_urls):
    driver.get(url)
    table = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="ohm_content"]/div[1]/table'),
        ),
    )
    soup = BeautifulSoup(table.get_attribute("outerHTML"), "html.parser")
    urls = list(OKTATAS_HU + link["href"] for link in soup.find_all("a", href=True))
    post_twenty_erettsegi_day_urls.update(urls)

# Scrape document links from post-twenty erettsegi day urls
post_twenty_file_urls = set()
for url in tqdm(post_twenty_erettsegi_day_urls):
    driver.get(url)
    table = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="ohm_content"]/div[1]/table'),
        ),
    )
    soup = BeautifulSoup(table.get_attribute("outerHTML"), "html.parser")
    urls = list(OKTATAS_HU + link["href"] for link in soup.find_all("a", href=True))
    post_twenty_file_urls.update(urls)

# Close the driver
driver.quit()

# Join the pre-twenty pdf and post-twenty file urls
unfiltered_urls = pre_twenty_pdf_urls | post_twenty_file_urls

# Filter out duplicates and unwanted mime types
filtered_urls = set()
filtered_filenames = set()
pattern = r"(\w)_(\w+)_(\d{2})(\w+)_(\w+)\.pdf"
for url in tqdm(unfiltered_urls):
    filename = os.path.basename(url)

    if filename in filtered_filenames:
        continue

    if match := re.search(pattern, filename):
        if match.group(2) in ["tort", "magyir", "mat"]:
            filtered_urls.add(url)
            filtered_filenames.add(filename)

# Create a directory for the pdf files
os.makedirs(".erettsegi", exist_ok=True)

# Download the pdf files to the directory
for url in tqdm(filtered_urls):
    filename = os.path.basename(url)
    response = requests.get(url)

    with open(f".erettsegi/{filename}", "wb") as f:
        f.write(response.content)
