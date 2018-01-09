from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

import scrapy

# item models from items.py -- don't forget to update these if you're adding new data keys to your scraper
from glassdoor.items import GlassdoorInterviewItem

class InterviewSpider(CrawlSpider):

    name = "glassdoor_interview"  # When we tell scrapy to "crawl", it uses this name variable to run this file
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
        Rule(LinkExtractor(allow=(), restrict_xpaths=("//li[@class='next']",)), callback="parse_search_results", follow = True),
    )

    def parse_start_url(self, response):
        for item in self.parse_search_results(response):
            yield item

    def parse_search_results(self, response):

        # Select parent elements containing each search result
        search_results = response.xpath("//div[@id='EmployerInterviews']//li[@class=' empReview cf ']")
        company_name = response.xpath("//div[@class='margTop']//div[@itemprop='child']//span[@itemprop='title']//text()").extract_first()

        # Iterate through each "item" in the search results
        for row in search_results:

            # Intiailize a new row item with our predefined model
            # (Dont forget to update this in items.py for capturing new elements!)
            search_item =  GlassdoorInterviewItem()

            search_item["company"] = company_name
            search_item["job_title"] = row.xpath(".//span[@class='reviewer']//text()").extract_first(default="N/A")
            search_item["review_date"] = row.xpath(".//time//text()").extract_first(default="N/A")
            search_item["offer_status"] = row.xpath("(.//div[@class='interviewOutcomes']//div[@class='cell']//span//text())[1]").extract_first(default="N/A")
            search_item["interview_experience"] = row.xpath("(.//div[@class='interviewOutcomes']//div[@class='cell']//span//text())[2]").extract_first(default="N/A")
            search_item["interview_difficulty"] = row.xpath("(.//div[@class='interviewOutcomes']//div[@class='cell']//span//text())[3]").extract_first(default="N/A")
            
            #FIX THESE
            search_item["application_proccess"] = row.xpath(".//p[contains(@class, 'applicationDetails')]//text()").extract_first(default="N/A")
            search_item["interview_description"] = row.xpath(".//p[contains(@class, 'interviewDetails')]//text()").extract()
            search_item["interview_questions"] = row.xpath(".//span[contains(@class, 'interviewQuestion')]//text()").extract()
    
            
            yield search_item