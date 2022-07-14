# TripAdvisor Reviews Scraper

Scraper of Tripadvisor reviews.

This Python class was designed for scraping comments of users of hotels of **Punta Cana**, but not limited,
may be used for scrap another useful data from others hotels or restaurants. 

![green-palms-raise-up-sky-sunny-beach](img/green-palms-raise-up-sky-sunny-beach.png?raw=true "Title")
<br/>
(Image credit: https://www.freepik.com/)


## What do you need?
- Python >= 3.6
- Google Chrome Browser
- Download Chromedrive from [here](https://chromedriver.storage.googleapis.com/index.html) and put it on ./bin/ folder.
  - This should be the same version of your Google Chrome Browser, check this in your browser > _About Google Chrome_ .
- Install Python packages from requirements file, either using pip, conda or virtualenv.
  - Recommended steps on mac (linux may be similar):
```shell
# create a virtual environment
python -m venv ./myvirtualenv
# enter to the recent created environment
source ./myvirtualenv/bin/activate
# look for the packages list
python -m pip list
# install requeriments
pip install -r requirements.txt

```
- Go to [tripadvisor](https://www.tripadvisor.com), click on Hotels, search for the name of a city and copy de url generated
by tripadvisor and paste in urls.txt local file.

## Example
```shell
python scraper.py --numhotel=10 --city=Florianopolis --maxcommentsperpage=10 --lang=Portuguese --outfile=my_dummy_file_data --verbose=1

```

## News [Jul/2022]
New function for scrap questions with their associate answers, the param is --qya.
### Example
python scraper.py --qya=1 --numhotel=30 --city=Miami_Beach --pagedepth=20 --lang=English --outfile=miami_beach --verbose=1 

## It is parameterizable

 - urls.txt file look like:
```
https://www.tripadvisor.com/Hotels-g303576-Florianopolis_State_of_Santa_Catarina-Hotels.html
```

## Disclaimer
 - This repository is part of ML's research portfolio on sentiment analysis.

## License
GNU GPLv3
