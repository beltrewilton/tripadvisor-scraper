# TripAdvisor Reviews Scraper

Scraper of Tripadvisor reviews.

This Python class was designed for scraping comments of users of hotels of Punta Cana, but not limited,
may be used for scrap another useful data from others hotels or restaurants. 


## What do you need?
- Python >= 3.6
- Download Chromedrive from [here](https://chromedriver.storage.googleapis.com/index.html). and put it on ./bin/ folder.
- Install Python packages from requirements file, either using pip, conda or virtualenv.
- Go to [tripadvisor](https://www.tripadvisor.com), locate Hotels, search for the name of a city and copy de url generated
by tripadvisor and paste in urls.txt local file.

## It is parameterizable
```python
scraper.work(landing_page=url, writer=writer, nums_hotel_to_scrape=60,
                              city='Florianopolis', comments_page_depth=25, lang_comments='Portuguese')
```


 - How many comments do you need? 
```python
    comments_page_depth=30
```
 - How many hotels do you need to investigate? 
 ```python
    nums_hotel_to_scrape=60
 ```
 - What is the language of interest of the comments?
 ```python
    lang_comments='Spanish'
 ```

## Disclaimer
 - This repository is part of ML's research portfolio on sentiment analysis.

## License
GNU GPLv3
