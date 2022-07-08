# -*- coding: utf-8 -*-
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
import traceback

URL_FILENAME = 'urls.txt'
MAX_WAIT = 10
MAX_RETRY = 10


class Tripadvisor:
    def __init__(self, driver_name, debug=False):
        self.debug = debug
        self.driver_name = driver_name
        self.driver = self.__get_driver()
        self.logger = self.__get_logger()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

        self.driver.close()
        self.driver.quit()

        return True

    def __rating(self, bubble):
        return int(bubble[7:8])

    def __hotel_urls(self, href, nums_hotel_to_scrape, key):
        hotel_urls = []
        for n in range(0, nums_hotel_to_scrape, 30):
            if n == 0:
                hotel_urls.append(href)
            else:
                hotel_urls.append(href.replace('-{}'.format(key), '-oa{}-{}'.format(n, key)))
        return hotel_urls

    def __full_list(self, landing_page, nums_hotel_to_scrape, key):
        hotel_review_pages = []

        for url in self.__hotel_urls(landing_page, nums_hotel_to_scrape, key):
            try:
                self.driver.get(url)
                print(url)
                time.sleep(np.random.uniform(6, 9))
                review_count = self.driver.find_elements_by_css_selector('a.review_count')
                # hrefs = [h.get_attribute("href") for h in review_count]
                for h in review_count:
                    hotel_review_pages.append(h.get_attribute("href"))
            except Exception as ex:
                print(ex)
                continue

        hotel_review_pages = list(filter(None, hotel_review_pages))
        return hotel_review_pages

    def work(self, landing_page, writer, nums_hotel_to_scrape, city, comments_page_depth=15, lang_comments='Spanish', verbose=0):
        hnum = 1
        hotel_review_pages = self.__full_list(landing_page, nums_hotel_to_scrape, city)
        try:
            for hotel_review in hotel_review_pages:
                print("{}/{} {}".format(hnum, len(hotel_review_pages), hotel_review))
                hnum += 1
                self.driver.get(hotel_review)
                time.sleep(np.random.uniform(6, 9))
                hotel_name = self.driver.find_element_by_css_selector('h1.QdLfr').text
                li_langs = self.driver.find_elements_by_css_selector('li.ui_radio')
                lang_found = False
                for li in li_langs:
                    lang = li.find_element_by_css_selector('span.ZmySZ').text
                    if lang == lang_comments:
                        lang_found = True
                        li.find_element_by_tag_name("span").click()
                        time.sleep(np.random.uniform(2, 5))
                        break

                if not lang_found:
                    print("No lang {} found for {}.".format(lang_comments, hotel_name))
                    continue

                total_reviews = self.driver.find_element_by_css_selector('span.iypZC').text.split(" ")[0].replace(',', '')
                if int(total_reviews) < 10:
                    continue

                comments_per_page = 5
                print(total_reviews)
                for i in range(comments_page_depth):
                    if i > 0:
                        if i * comments_per_page >= int(total_reviews):
                            print("low comments {} {}".format(total_reviews, hotel_name))
                            break

                        try:
                            next = self.driver.find_element_by_xpath("//span[@class='pageNum current disabled']/following-sibling::a")
                            print("{} :: {}".format(i + 1, next.get_attribute("href")))
                            next.click()
                            time.sleep(np.random.uniform(3, 6))
                        except Exception as ex:
                            print(ex)
                            break

                    reviews = self.driver.find_elements_by_css_selector('div.YibKl')
                    for rev in reviews:
                        wrote = None
                        try:
                            wrote = rev.find_element_by_css_selector('span.teHYY').text.replace('Date of stay: ', '')
                        except Exception as ex:
                            print(ex)

                        location = None
                        try:
                            location = self.driver.find_element_by_xpath("//span[@class='default LXUOn small']").text
                        except Exception as ex:
                            print(ex)

                        try:
                            title = rev.find_element_by_css_selector('a.Qwuub').find_element_by_tag_name("span").find_element_by_tag_name("span").text
                            comment = rev.find_element_by_css_selector('q.QewHA').find_element_by_tag_name("span").text
                            rating = rev.find_element_by_css_selector('div.Hlmiy').find_element_by_tag_name("span").get_attribute("class").split(" ")[1]
                            rating = self.__rating(rating)
                            if verbose:
                                print("{}\t{}\t{}\t{}\t{}\t{}".format(hotel_name, location, wrote, rating, title, comment))
                            writer.writerow([hotel_name, location, wrote, rating, title, comment])
                        except Exception as ex:
                            print(ex)
        except Exception as ex:
            print(ex)

    def __get_logger(self):
        # create logger
        logger = logging.getLogger('tripadvisor-scraper')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        fh = logging.FileHandler('ta-scraper.log')
        fh.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatter to ch
        fh.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(fh)

        return logger

    def __get_driver(self):
        options = Options()
        if not self.debug:
            options.add_argument("--headless")
        options.add_argument("--window-size=1366,768")
        options.add_argument("--disable-notifications")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en_GB'})
        input_driver = webdriver.Chrome(executable_path='./bin/{}'.format(self.driver_name), chrome_options=options)

        return input_driver
