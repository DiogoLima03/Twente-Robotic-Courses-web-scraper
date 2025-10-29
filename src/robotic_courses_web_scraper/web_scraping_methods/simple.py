import pandas as pd


def simple(url: str):
    # returns a list of DataFrames found on the page
    tables = pd.read_html(url, header=None)          # optionally: pd.read_html(url, match="Table Title")
    print(f"Found {len(tables)} tables")

    df = tables[0]                      # pick the right one
    df.to_csv("table.csv", index=False, header=False)
    print(df.head())

