import logging
import scrapy
from lxml import html
from scrapy import loader
from tutorial.items import AppItem
from scrapy.loader import ItemLoader
from urllib.parse import urlparse
class AppSpider(scrapy.Spider):
    name = 'apps'
    keyword = 'facebook'
    start_urls = [
                  'https://play.google.com/store/search?q=' + keyword,
                  'https://search.f-droid.org/?q='+ keyword + '&lang=en',
                  'https://fossdroid.com/s.html?q='+ keyword,
                  'https://en.uptodown.com/android/search/' + keyword,
                  'https://www.appsapk.com/?s=' + keyword
                 ]
    domains = [
                'play.google.com',
                'f-droid.org',
                'fossdroid.com',
                'uptodown.com',
                'appsapk.com'
              ]
    app_item = AppItem()
    def start_requests(self):
        for start_url in self.start_urls:
             yield scrapy.Request(url=start_url, callback=self.parse)
    # Parse from the root URL
    def parse(self, response):
        # Contain all the link of the search results
        app_links = []
        # Get all the urls contain the keywords of the search results
        for res in response.xpath('//*[contains(@href, "'+ self.keyword +'")]/@href'):
            app_links.append(res.get())
        # Choosing parser
        url = response.url
        logging.info(url)
        domain = urlparse(url).netloc
        logging.info(domain)
        callback = self.parse_app 
        if self.domains[1] in url: 
            callback = self.parse_Fdroid
        elif self.domains[2] in url:
            callback = self.parse_FossDroid
        elif self.domains[3] in url:
            callback = self.parse_UpToDown
        elif self.domains[4] in url:
            callback = self.parse_AppsApk
              
        # Scrape all the links in the search result
        for link in app_links:
            if link is not None:
                absolute_link = response.urljoin(link)
                logging.info(absolute_link)
                yield scrapy.Request(absolute_link, callback=callback)
                
        # Add Scrape for next page or See more
        if self.domains[0] in url:
            # Get See More in Google App Store
            see_more = response.xpath('//a[contains(text(),"See more")]/@href').get()
            if see_more:                    
                absolute_link = response.urljoin(see_more)
                yield scrapy.Request(absolute_link, callback=self.parse)
                
        if self.domains[3] in url:
            see_more = response.xpath('//a[contains(@class, "more")]/@href').get()
            if see_more:
                absolute_link = response.urljoin(see_more)
                yield scrapy.Request(absolute_link, callback=self.parse)
            
    # Parse each app in the search results
    # Parse Google Play
    def parse_app(self, response):
        relative_path = '//span[contains(translate(text(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "' + self.keyword + '")]'
        url = response.url
        page = scrapy.Request(url)
        root = html.fromstring(response.xpath('//*').get())
        # Generate path to an element
        tree = root.getroottree()
        destination = root.xpath(relative_path)
        path = tree.getpath(destination[0]) if len(destination) else ''
        # Generate Title, an App should have title
        title = response.xpath(relative_path + '/text()').get()
        title = title if title else ''
        # Generate Developer
        developer = response.xpath('//div[contains(text(), "Offered By")]/following-sibling::span/div/span/text()').get()   
        developer = developer if developer else ''
        # Generating App Item
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', url)
        loader.add_value('path_title', path)
        loader.add_value('title', title)
        loader.add_value('developer', developer)
        loader.add_value('distributor', 'Google Play')
        yield loader.load_item()

    # Parse Fdroid
    def parse_Fdroid(self, response):
        relative_path = '//h3[contains(translate(text(),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"), "' + self.keyword + '")]'
        url = response.url
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', response.url)
        page = scrapy.Request(url)
        root = html.fromstring(response.xpath('//*').get())
        # Generate path to an element
        tree = root.getroottree()
        destination = root.xpath(relative_path)
        path = tree.getpath(destination[0]) if len(destination) else ''
        # Generate Title, an App should have title
        title = response.xpath(relative_path + '/text()').get()
        title = title if title else ''
        # Generate Developer
        developer = response.xpath('//li[contains(text(),"Author")]/a/text()').get()   
        developer = developer if developer else ''
        # Generating App Item
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', url)
        loader.add_value('path_title', path)
        loader.add_value('title', title)
        loader.add_value('developer', developer)
        loader.add_value('distributor', 'F-Droid')
        yield loader.load_item()
    
    # Parse FossDroid
    def parse_FossDroid(self, response):
        logging.info("Scraping FossDroid")
        relative_path = '//h1[contains(@class, "fd-application_title")]'
        url = response.url
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', response.url)
        page = scrapy.Request(url)
        root = html.fromstring(response.xpath('//*').get())
        # Generate path to an element
        tree = root.getroottree()
        destination = root.xpath(relative_path)
        path = tree.getpath(destination[0]) if len(destination) else ''
        # Generate Title, an App should have title
        title = response.xpath(relative_path + '/text()').get()
        title = title if title else ''
        # Generate Developer
        developer = ''
        # Generating App Item
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', url)
        loader.add_value('path_title', path)
        loader.add_value('title', title)
        loader.add_value('developer', developer)
        loader.add_value('distributor', 'FossDroid')
        yield loader.load_item()
        
    # Parse UpToDown
    def parse_UpToDown(self, response):
        logging.info("Scraping UpToDown")
        logging.info(response.url)
        relative_path = '//h1[contains(@id, "detail-app-name")]'
        url = response.url
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', response.url)
        page = scrapy.Request(url)
        root = html.fromstring(response.xpath('//*').get())
        # Generate path to an element
        tree = root.getroottree()
        destination = root.xpath(relative_path)
        path = tree.getpath(destination[0]) if len(destination) else ''
        # Generate Title, an App should have title
        title = response.xpath(relative_path + '/text()').get()
        title = title if title else ''
        # Generate Developer
        developer = response.xpath('//a[contains(@id, "author-link")]/text()').get()
        developer = developer if developer else ''
        # Generating App Item
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', url)
        loader.add_value('path_title', path)
        loader.add_value('title', title)
        loader.add_value('developer', developer)
        loader.add_value('distributor', 'UpToDown')
        yield loader.load_item()
        
    # Parse AppsApk
    def parse_AppsApk(self, response):
        logging.info("Scraping AppsApk")
        logging.info(response.url)
        relative_path = '//h1[contains(@class, "entry-title")]'
        url = response.url
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', response.url)
        page = scrapy.Request(url)
        root = html.fromstring(response.xpath('//*').get())
        # Generate path to an element
        tree = root.getroottree()
        destination = root.xpath(relative_path)
        path = tree.getpath(destination[0]) if len(destination) else ''
        # Generate Title, an App should have title
        title = response.xpath(relative_path + '/text()').get()
        title = title if title else ''
        # Generate Developer
        developer = response.xpath('//strong[contains(text(), "Developed By")]/../text()').get()
        developer = developer if developer else ''
        # Generating App Item
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', url)
        loader.add_value('path_title', path)
        loader.add_value('title', title)
        loader.add_value('developer', developer)
        loader.add_value('distributor', 'AppsApk')
        yield loader.load_item()
    
    
            