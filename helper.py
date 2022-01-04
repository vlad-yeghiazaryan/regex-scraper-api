# custom functions
from scraper import Scraper

# disabling certificate
import urllib3
urllib3.disable_warnings()

# running scraper
def scrape_page(urls, query_list):
  pages = Scraper(urls, list(query_list.values()))
  pages.scrape()

  # rename table columns
  inverted_query_list = {v: k for k, v in query_list.items()}
  table = pages.table.rename(columns=inverted_query_list)
  return table.to_dict('records')
