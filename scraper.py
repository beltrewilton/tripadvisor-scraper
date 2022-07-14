# -*- coding: utf-8 -*-

from tripadvisor import Tripadvisor
import argparse
import csv


HEADER = ['hotel_name', 'location', 'wrote', 'rating', 'title', 'comment']
HEADER_QUESTION = ['id', 'hotel_name', 'user', 'city', 'date', 'contrib', 'help_votes', 'question']
HEADER_ANSWER = ['question_id', 'user', 'date', 'answer', 'votes']


def csv_writer(path='data/', outfile='florianopolis_data', header=HEADER):
    targetfile = open(path + outfile + '.csv', mode='w', encoding='utf-8', newline='\n')
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(header)
    return writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tripadvisor scraper.')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--numhotel', type=int, default=5, help='the max nums of hotel to being scraped.')
    parser.add_argument('--city', type=str, default='Florianopolis', help='city name')
    parser.add_argument('--pagedepth', type=int, default=5, help='How many pages in the hotel landing to scrap.')
    parser.add_argument('--lang', type=str, default='Portuguese', help='The lang of comment to being scraped.')
    parser.add_argument('--outfile', type=str, default='dummy_data', help='Out data file name')
    parser.add_argument('--qya', type=int, default=0, help='Q&A scrap')
    parser.add_argument('--verbose', type=int, default=0, help='Print the data in the terminal (0 = no print, 1 = print).')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Debug mode: chromedriver with graphical part')
    parser.set_defaults(place=False, debug=False)

    args = parser.parse_args()

    # store reviews/Q&A in CSV file
    writer = None
    writer_question = None
    writer_answer = None

    if args.qya == 1:
        writer_question = csv_writer(outfile='{}_questions'.format(args.outfile), header=HEADER_QUESTION)
        writer_answer = csv_writer(outfile='{}_answers'.format(args.outfile), header=HEADER_ANSWER)
    else:
        writer = csv_writer(outfile=args.outfile, header=HEADER)

    with Tripadvisor(driver_name='chromedriver', debug=args.debug) as scraper:
        with open(args.i, 'r') as url_file:
             for url in url_file:
                 if args.qya == 1:
                     scraper.work_qya(landing_page=url, writer=writer_question, writer_ans=writer_answer,
                                      nums_hotel_to_scrape=args.numhotel,  city=args.city,
                                      comments_page_depth=args.pagedepth, verbose=args.verbose)
                 else:
                    scraper.work(landing_page=url, writer=writer, nums_hotel_to_scrape=args.numhotel,
                                     city=args.city, comments_page_depth=args.pagedepth,
                                     lang_comments=args.lang, verbose=args.verbose)

