# Hand gestures to HomeAssist commands

This pyhton app uses web scrapping to get all the Robotic Courses from canvas UT website.

It presents 3 methods. 
## Simple, used for data that is not rendered with JS. 
## Precise control, used for target a specific table by id/class or clean cells, uses requests + BeautifulSoup.
## Advance, if rendered by JS, uses Selenium


## Instalation instructions
```
pip install -e .
```

## Using the library
```
poetry env use 3.13
poetry install
poetry run scraper (simple or precise or advance) (url: https://example.com)
```

