from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def advance(url: str):
    opts = Options()
    opts.add_argument("--headless=new")
    driver = webdriver.Chrome(options=opts)
    driver.get(url)

    # Wait for the table to appear
    table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "table#results"))
    )

    # Pull rows
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    data = []
    for r in rows:
        cells = [c.text.strip() for c in r.find_elements(By.CSS_SELECTOR, "th,td")]
        data.append(cells)

    # Header
    ths = table.find_elements(By.CSS_SELECTOR, "thead th")
    if ths:
        headers = [th.text.strip() for th in ths]
    else:
        headers = [f"col{i+1}" for i in range(len(data[0]))]

    driver.quit()

    df = pd.DataFrame(data, columns=headers)
    df.to_csv("table.csv", index=False)
    print(df.head())
