from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import scrapy

# item models from items.py -- don't forget to update these if you're adding new data keys to your scraper
from recipes.items import RecipesItemSearch

class InterviewSpider(CrawlSpider):

    name = "interview"  # When we tell scrapy to "crawl", it uses this name variable to run this file
    allowed_domains = ["glassdoor.com"]
    start_urls = [
        "https://www.glassdoor.com/Interview/General-Assembly-Interview-Questions-E459214.htm"
    ]

    #  The last rule that is uncommented, will tell the spider to continiously look for the next page to scrape.
    #  If it finds another page to scrape, it will run the parse_search_results() method on it and continually capture new records
    rules = (
        # Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), follow = True),
        # //a/strong[contains(text(), 'Next >')]/../@href"

        #  The rule will tell the spider to continiously look for the next page to scrape.
        #  If it finds another page to scrape, it will run the parse_search_results() method on it and continually capture new records
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="the-next-page"]',)), callback="parse_search_results", follow = True),
    )


    def parse_search_results(self, response):

        # Select parent elements containing each search result
        search_results = response.xpath("//div[@id='EmployerInterviews']")

        # Iterate through each "item" in the search results
        for row in search_results:

            # Intiailize a new row item with our predefined model
            # (Dont forget to update this in items.py for capturing new elements!)
            search_item =   GlassdoorInterviewItem()
            search_item["job_title"] = row.xpath(".//div[@class='tbl fill reviewHdr']//span[@class='reviewer']").extract_first(default="N/A")
    
            # Try to extract the data for catetory, ratings, no. of reviews, image source
            
            yield search_item