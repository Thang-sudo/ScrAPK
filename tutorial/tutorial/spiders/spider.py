import logging
import scrapy
from lxml import html
from tutorial.items import AppItem
from scrapy.loader import ItemLoader

class AppSpider(scrapy.Spider):
    name = 'apps'
    keyword = 'instagram'
    start_urls = ['https://play.google.com/store/search?q=' + keyword]
    app_item = AppItem()
    # Parse from the root URL
    def parse(self, response):
        # Contain all the link of the search results
        app_links = []
        # Get all the urls contain the keywords of the search results
        for res in response.xpath('//*[contains(@href, "'+ self.keyword +'")]/@href'):
            app_links.append(res.get())
        # Scrape all the links in the search result 
        for link in app_links:
            if link is not None:
                absolute_link = response.urljoin(link)
                yield scrapy.Request(absolute_link, callback=self.parse_app)
        
    # Parse each app in the search results
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
        title = response.xpath(relative_path).get()
        title = title if title else ''
        # Generate Developer
        developer = response.xpath('//div[contains(text(), "Offered By")]/following-sibling::span/div/span').get()   
        developer = developer if developer else ''
        # Generating App Item
        loader = ItemLoader(item=AppItem(), response=response)
        loader.add_value('link', url)
        loader.add_value('path_title', path)
        loader.add_value('title', title)
        loader.add_value('developer', developer)
        yield loader.load_item()
            