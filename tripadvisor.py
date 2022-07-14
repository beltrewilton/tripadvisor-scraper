# -*- coding: utf-8 -*-
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
import traceback
import re

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
        for n in range(0, nums_hotel_to_scrape, 30):  # 30 numbers of hotels in the landing-page
            if n == 0:
                hotel_urls.append(href)
            else:
                hotel_urls.append(href.replace('-{}'.format(key), '-oa{}-{}'.format(n, key)))
        return hotel_urls

    def __full_list(self, landing_page, nums_hotel_to_scrape, key):
        hotel_review_pages = []

        for k, url in enumerate(self.__hotel_urls(landing_page, nums_hotel_to_scrape, key)):
            try:
                self.driver.get(url)
                print(url)
                time.sleep(np.random.uniform(6, 9))
                review_count = self.driver.find_elements_by_css_selector('a.review_count')
                if len(review_count) == 0:
                    review_count = self.driver.find_elements_by_css_selector('li.ui_column a')  # work for Finland :/
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
                            # print("{} :: {}".format(i + 1, next.get_attribute("href")))
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



    # https://www.tripadvisor.com/Hotels-g45963-Las_Vegas_Nevada-Hotels.html
    def work_qya(self, landing_page, writer, writer_ans, nums_hotel_to_scrape, city, comments_page_depth=15,  verbose=0):
        hnum = 1
        hotel_review_pages = self.__full_list(landing_page, nums_hotel_to_scrape, city)
        idx = 1
        for hotel_review in hotel_review_pages:
            try:
                print("{}/{} {}".format(hnum, len(hotel_review_pages), hotel_review))
                hnum += 1
                self.driver.get(hotel_review.replace('#REVIEWS', ''))
                time.sleep(np.random.uniform(4, 7))
                hotel_name = self.driver.find_element_by_css_selector('h1.QdLfr').text
                try:
                    self.driver.find_element_by_css_selector('span.test-target-tab-Questions').click()  # swich to Q&A
                    time.sleep(np.random.uniform(4, 7))
                except Exception as ex:  # Element is not clickable at point
                    print(ex)
                    continue

                total_questions = 0
                try:
                    total_questions = self.driver.find_element_by_css_selector('a.weEPs').text.split(' ')[2]
                except Exception as ex:
                    print(ex)  # looks less than 5 q.
                    continue  # not enough q.
                question_per_page = 5
                for i in range(comments_page_depth):
                    if i > 0:
                        if i * question_per_page >= int(total_questions):
                            print("low questions in this page {} {}".format(total_questions, hotel_name))
                            break

                        try:
                            next = self.driver.find_element_by_xpath(
                                "//span[@class='pageNum current disabled']/following-sibling::span")
                            print("{} :: {}".format(i + 1, next.get_attribute("href")))
                            next.click()
                            time.sleep(np.random.uniform(5, 8))
                        except Exception as ex:
                            print(ex)
                            break

                    questions = self.driver.find_elements_by_css_selector('div.YibKl')
                    for quest in questions:
                        idx += 1
                        question = quest.find_element_by_css_selector('a.ncbar').text
                        qheader = quest.find_element_by_css_selector('div.cRVSd span').text.split(' asked a question ')
                        quser = qheader[0]
                        qdate = qheader[1]
                        qcity = None
                        try:
                            qcity = quest.find_element_by_css_selector('span.RdTWF span').text
                        except Exception as ex:
                            print(ex)
                        helps = None
                        qcontrib = None
                        qhelpvotes = None
                        try:
                            helps = quest.find_elements_by_css_selector('span.yRNgz')
                            qcontrib = helps[0].text
                            qhelpvotes = helps[1].text
                        except Exception as ex:
                            print(ex)

                        responder = []
                        try:
                            quest.find_element_by_css_selector('a.uRJQp').click()  # show all comments
                            time.sleep(np.random.uniform(4, 7))
                            resp = quest.find_elements_by_css_selector('div.XoYbv')

                            for i in range(1, len(resp)):
                                resp_dict = {}
                                ruser = None
                                try:
                                    ruser = resp[i].find_element_by_css_selector('div.cRVSd a').text
                                    resp_dict.update({'user': ruser})
                                    resp_dict.update({'question_id': idx})
                                except Exception as ex:
                                    print(ex)
                                rdate = None
                                try:
                                    rdate = resp[i].find_element_by_css_selector('div.iHmzx span').text.replace(' |', '')
                                    resp_dict.update({'date': rdate})
                                except Exception as ex:
                                    print(ex)
                                ransw = None
                                try:
                                    ransw = resp[i].find_element_by_css_selector('div.roHJW').text
                                    resp_dict.update({'ans': ransw})
                                except Exception as ex:
                                    print(ex)
                                rvotes = None
                                try:
                                    rvotes = resp[i].find_element_by_css_selector('span.FzkHe').text  # 1 vote, 200 votes
                                    rvotes = re.sub('\ vote.?', '', rvotes)
                                    resp_dict.update({'votes': rvotes})
                                except Exception as ex:
                                    print(ex)
                                responder.append(resp_dict)
                        except Exception as ex:
                            print(ex)
                            ruser = None
                            resp_dict = {}
                            try:
                                ruser = quest.find_elements_by_css_selector('div.cRVSd a')[1].text
                                resp_dict.update({'user': ruser})
                                resp_dict.update({'question_id': idx})
                            except Exception as ex:
                                print(ex)
                            rdate = None
                            try:
                                rdate = quest.find_element_by_css_selector('div.iHmzx span').text.replace(' |', '')
                                resp_dict.update({'date': rdate})
                            except Exception as ex:
                                print(ex)
                            ransw = None
                            try:
                                ransw = quest.find_element_by_css_selector('div.roHJW').text
                                resp_dict.update({'ans': ransw})
                            except Exception as ex:
                                print(ex)
                            rvotes = None
                            try:
                                rvotes = quest.find_element_by_css_selector('span.FzkHe').text.replace(' votes', '')
                                resp_dict.update({'votes': rvotes})
                            except Exception as ex:
                                print(ex)
                            responder.append(resp_dict)

                        if verbose:
                            print('{}\t{}\t{}\t{}\t{}\t{}\n{}\n'.format(idx, hotel_name, quser, qcity, qdate, qcontrib,
                                                                        qhelpvotes, question, responder))
                        writer.writerow([idx, hotel_name, quser, qcity, qdate, qcontrib, qhelpvotes, question])
                        # ['id', 'hotel_name', 'user', 'city', 'date', 'contrib', 'help_votes', 'question']
                        for r in responder:
                            try:
                                writer_ans.writerow([r['question_id'], r['user'], r['date'], r['ans'], r['votes']])
                            except Exception as ex:
                                pass
            except Exception as ex:
                errors = ['crash', 'renderer', 'disconnected', 'unknown']
                if any(x in str(ex) for x in errors):
                    time.sleep(np.random.uniform(10, 15))
                    try:
                        self.driver.close()
                        self.driver.quit()
                    except Exception as ex:
                        pass
                    print('Waiting for new connection.......')
                    time.sleep(np.random.uniform(100, 120))
                    self.driver = self.__get_driver()
                else:
                    print('Dead:', ex)


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
