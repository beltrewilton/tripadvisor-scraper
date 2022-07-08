# TripAdvisor Reviews Scraper

Scraper of Tripadvisor reviews.

This Python class was designed for scraping comments of users of hotels of **Punta Cana**, but not limited,
may be used for scrap another useful data from others hotels or restaurants. 

![green-palms-raise-up-sky-sunny-beach](img/green-palms-raise-up-sky-sunny-beach.png?raw=true "Title")


## What do you need?
- Python >= 3.6
- Google Chrome Browser
- Download Chromedrive from [here](https://chromedriver.storage.googleapis.com/index.html) and put it on ./bin/ folder.
  - This should be the same version of your Google Chrome Browser, check this in your browser > _About Google Chrome_ .
- Install Python packages from requirements file, either using pip, conda or virtualenv.
- Go to [tripadvisor](https://www.tripadvisor.com), click on Hotels, search for the name of a city and copy de url generated
by tripadvisor and paste in urls.txt local file.

## It is parameterizable

 - urls.txt file look like:
```
https://www.tripadvisor.com/Hotels-g303576-Florianopolis_State_of_Santa_Catarina-Hotels.html
```

```python
scraper.work(landing_page=url, writer=writer, nums_hotel_to_scrape=60,
                              city='Florianopolis', comments_page_depth=25, lang_comments='Portuguese')
```
  - City name is an important key:
```python
    city='Florianopolis'
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
  - Don't forget the change the **outfile** file name:
```python
def csv_writer(path='data/', outfile='florianopolis_data'):
    targetfile = open(path + outfile + '.csv', mode='w', encoding='utf-8', newline='\n')
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(HEADER)

    return writer
```

## Disclaimer
 - This repository is part of ML's research portfolio on sentiment analysis.

## License
GNU GPLv3
