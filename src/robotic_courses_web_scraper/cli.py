import argparse
from .app import run

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="Robotics Courses Scraper",
        description="Scrapes and processes robotics course data from the University of Twente website."
    )

    parser.add_argument(
        "method",
        nargs="?",
        choices=["simple", "precise", "advanced"],
        default="simple",
        help="Scraping method: 'simple' (fast), 'precise' (balanced), or 'advanced' (detailed). Defaults to 'simple'."
    )

    parser.add_argument(
        "url",
        nargs="?",
        default="https://www.utwente.nl/en/rob/programme-information/all_robotics_courses/",
        help="URL of the page to scrape. Defaults to the UT Robotics course overview."
    )

    args = parser.parse_args()
    code = run(args.url, args.method)
    raise SystemExit(code)
