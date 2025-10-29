from .web_scraping_methods import *
from pathlib import Path
import pandas as pd
import numpy as np

def run(url: str, method: str):
    ### web scrape the data ###
    
    table_path = Path("table.csv")
    
    # Check if the CSV already exists
    if not table_path.exists():
        print("Fetching table from website...")
        if method == "simple":
            simple(url)
        elif method == "precise":
            precise(url)
        elif method == "advance":
            advance(url)
        else:
            print("No method available selected.")
            return
    else:
        print("Found existing 'table.csv' — skipping fetch.")
    
    ### Treat the data ###
    df = pd.read_csv("table.csv", header=None)
    
    # removing the first row (it's just numbers 0 1 2 3) and making header row 2 ###########
    df.columns = df.iloc[1]
    df = df[2:]
    df.reset_index(drop=True, inplace=True) # Clean up the index
    ########################################################################################
    
    # make sure it is imported with the right type ###########################
    df.iloc[:, 0] = df.iloc[:, 0].astype(int) # course code
    df.iloc[:, 1] = df.iloc[:, 1].astype(str) # quartile (ex: 1A, 1B, 2A, 2B)
    df.iloc[:, 2] = df.iloc[:, 2].astype(str) # course name
    df.iloc[:, 3] = df.iloc[:, 3].astype(str) # course type
    ##########################################################################
    
    # Normalize Quartile text: uppercase, remove spaces, unify commas
    q = (
        df["Quartile"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.replace(r"\s+", "", regex=True)  # e.g. "1B, 2A" -> "1B,2A"
    )

    # One-hot encode quartile memberships
    quartiles = q.str.get_dummies(sep=",")

    # Ensure all expected columns exist and are boolean
    expected = ["1A", "1B", "2A", "2B"]
    for col in expected:
        if col not in quartiles.columns:
            quartiles[col] = False
    quartiles = quartiles[expected].astype(bool)

    # Rename for clarity
    quartiles.columns = [f"Q{c}" for c in quartiles.columns]

    # Insert after first column (course code)
    cols = df.columns.tolist()
    insert_pos = 1  # right after the course code column
    for col in reversed(quartiles.columns):  # reverse so they appear in order
        df.insert(insert_pos, col, quartiles[col])
        
    df.drop(columns=["Quartile"], inplace=True)

    print("Added columns Q1A, Q1B, Q2A, Q2B and dropped 'Quartile'.")
    #################################################################################################
    
    ### formating course type column to just elective, compulsory and profile and then add coluns for specifics ######
    s = df["Course Type"].fillna("").astype(str).str.strip()

    # fix common typos and normalize
    s = (s.str.replace(r"\s+", " ", regex=True)
        .str.replace("Resarch", "Research", regex=False)
        .str.replace("Proflie", "Profile", regex=False))
    df_courseType = s
    
    # normalized base type
    df["Course Type"] = np.where(
        s.str.startswith("Compulsory"),
        "Compulsory",
        np.where(
            s.str.startswith("Profile"),
            "Profile",
            np.where(s.str.startswith("Elective"), "Elective", "Unknown")
        )
    )

    # grab the stuff inside parentheses and normalize for matching
    inside = (s.str.extract(r"\((.*?)\)", expand=False)
                .fillna("")
                .str.upper()
                .str.replace("RESEARCH", "", regex=False)
                .str.replace(r"\s+", "", regex=True))

    # boolean flags for profiles
    df["MPAI"]   = inside.str.contains(r"\bMPAI\b", regex=True)
    df["ASAI"]   = inside.str.contains(r"\bASAI\b", regex=True)
    df["HRISAI"] = inside.str.contains(r"\bHRISAI\b", regex=True)
    
    track_cols = ["MPAI", "ASAI", "HRISAI"]

    # find rows where all three are False
    mask = ~df[track_cols].any(axis=1)

    # replace False → "Unknown" in those rows
    df.loc[mask, track_cols] = "Unknown"

    print("Formated column Course Type and added columns MPAI, ASAI, HRISAI")
    ################################################################################################################################
    
    # add column for Profile Type #################################################################
    
    s = df_courseType

    # new column Profile Type
    df["Profile Type"] = np.select(
        [
            (df["Course Type"] == "Profile") & s.str.contains(r"\bRESEARCH\b", case=False),
            (df["Course Type"] == "Profile") & s.str.contains(r"\bDESIGN\b", case=False),
            (df["Course Type"] == "Profile") & s.str.contains(r"I&E", case=False)
        ],
        ["Research", "Design", "I&E"],
        default="None"
    )
    ###############################################################################################
    
    # Save to Excel (.xlsx)
    df.to_excel("Robotic Courses.xlsx", index=False)   # openpyxl is auto-picked
    print("Saved table to Robotic Courses.xlsx")
    
    
    
    
    