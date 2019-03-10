import Main_crawler
import logging


def main():
    # set up logger
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename="./scrape_web_report.log", level=logging.INFO, format=log_format, filemode='w')

    # start crawl and store json data into file
    start = 'https://en.wikipedia.org/wiki/George_Clooney#Filmography'
    fname = "small_data.json"
    Main_crawler.bfs_crawl(start, fname)


if __name__ == "__main__":
    main()

