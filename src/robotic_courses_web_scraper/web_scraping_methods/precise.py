import requests
from bs4 import BeautifulSoup
import pandas as pd

def precise(url:str):
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    # Example selectors – adjust:
    table = soup.select_one("table#prices")  # or ".table.table-striped", "table[data-name='results']"
    assert table, "Table not found"

    # Extract header
    thead = table.find("thead")
    if thead:
        headers = [th.get_text(strip=True) for th in thead.select("th")]
    else:
        # fallback: first row as header
        first_row = table.select_one("tr")
        headers = [c.get_text(strip=True) for c in first_row.find_all(["th","td"])]

    # Extract rows
    rows = []
    for tr in table.select("tbody tr") or table.select("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all(["td","th"])]
        # pad/truncate to header length if needed
        if len(cells) < len(headers):
            cells += [""] * (len(headers) - len(cells))
        rows.append(cells[:len(headers)])

    df = pd.DataFrame(rows, columns=headers)
    df.to_csv("table.csv", index=False)
    print(df.head())
