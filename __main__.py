from helper import scrape_page

def main(request):
  scraped_data = scrape_page(request['urls'], request['query_list'])
  
  # Response message
  return {'scraped_data': scraped_data}
