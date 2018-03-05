# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from home_scrapper.items import HomeScrapperItem
from urlparse import urlparse


class homeScrapperSpider(scrapy.Spider):
    name = 'homescrapper'
    url_input = raw_input("Enter the URL:  ")
	
    # The domains that are allowed for scraping. Get the domain name from the URL
    allowed_domains = [urlparse(url_input).hostname[4:]]

    # The URL to start scraping from
    start_urls = [url_input]
	
    # Count for 25 scraped URLs
    count = 0
    
    # Spider Rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_urls"
        )
    ]

    # Method to send request to the start_url and call the parse funtion 
    def start_requests(self):
	for url in self.start_urls:
		yield scrapy.Request(url, callback=self.parse_urls, dont_filter=True)


    # Method for parsing items from the retrieved URLs
    def parse_urls(self, response):
        # The list of items that are found on the particular page
        items = []
        # Extract canonicalized and unique URLs
	links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # Follow each link
        for link in links:
            # Check whether the domain is allowed
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            # If allowed and number of URLs < 25, store the URL in the scrape object
            if ((is_allowed) and (self.count < 25)):
		item = HomeScrapperItem()
		item['url_names'] = link.url
		items.append(item)
		self.count +=1
        # Return all the found URLs 
        return items
