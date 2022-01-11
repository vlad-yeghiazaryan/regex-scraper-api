#  Main
import numpy as np
import pandas as pd
import regex
import time
import random
from datetime import datetime

# Scraping
import requests
import concurrent.futures
from fp.fp import FreeProxy

class Scraper(object):
    def __init__(self, urls, page_data_func, MAX_THREADS=30, wait_time=0.1, use_proxies=False, proxy_timeout=0.3, regex_group_number=0):
        self.urls = urls
        self.MAX_THREADS = MAX_THREADS
        self.wait_time = wait_time
        self.threads = min(self.MAX_THREADS, len(self.urls))
        self.use_proxies = use_proxies
        self.proxy_timeout = proxy_timeout
        self.final_url = self.urls[-1]
        self.page_data_func = page_data_func if type(page_data_func)!=list else self.regex_search(page_data_func)
        self.group_number = regex_group_number
        self.raw_data = []
        self.dateToday = datetime.today().strftime('%Y-%m-%d')

    def newProxy(self):
        random_country = random.choice(['US', 'RU', 'JP', 'HK', 'LB', 'FR', 'CA','DE', 'SG', 'HK'])
        proxy = FreeProxy(country_id=random_country,
                          timeout=self.proxy_timeout, rand=True).get()
        proxyDict = {
            "http": proxy
        }
        return proxyDict

    def regex_search(self, query_list):
        def regex_page_search(page):
            if page != None:
                if page.ok:
                    result = {'date':self.dateToday, 'url':page.url}
                    for query in query_list:
                        try:
                            res = regex.search(query, str(page.content)).group(self.group_number)
                        except:
                            res = np.NaN
                        result.update({query: res})
            else:
                result = {}
            return result
        return regex_page_search

    def getPage(self, url):
        user_agent = random.choice(['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', 
                      'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'])
        headers = {'User-Agent': user_agent}
        try:
            proxy = None
            if self.use_proxies:
                proxy = self.newProxy()
            page = requests.get(url, proxies=proxy, headers=headers)
            time.sleep(self.wait_time)
            return page if page.ok else page
        except:
            return None

    def scrape_page(self, url):
        page = self.getPage(url)
        page_data = self.page_data_func(page)
        self.raw_data.append(page_data)

    @property
    def table(self):
        scraped_table = pd.DataFrame(self.raw_data)
        return scraped_table

    def scrape(self):
        # write scrapped data into json file
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.scrape_page, self.urls)
        print('Scraping complete')
