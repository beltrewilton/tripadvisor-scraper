# -*- coding: utf-8 -*-

from tripadvisor import Tripadvisor
import argparse
import csv


HEADER = ['hotel_name', 'location', 'wrote', 'rating', 'title', 'comment']


def csv_writer(path='data/', outfile='florianopolis_data'):
    targetfile = open(path + outfile + '.csv', mode='w', encoding='utf-8', newline='\n')
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(HEADER)

    return writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tripadvisor scraper.')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Debug mode: chromedriver with graphical part')
    parser.set_defaults(place=False, debug=False)

    args = parser.parse_args()

    # store reviews in CSV file
    writer = csv_writer()

    with Tripadvisor(driver_name='chromedriver', debug=args.debug) as scraper:
        with open(args.i, 'r') as url_file:
             for url in url_file:
                 scraper.work(landing_page=url, writer=writer, nums_hotel_to_scrape=5,
                              city='Florianopolis', comments_page_depth=5, lang_comments='Portuguese')
