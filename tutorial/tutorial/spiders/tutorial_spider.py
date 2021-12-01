import scrapy

class TutorialSpider(scrapy.Spider):
    name = 'tutorial'
    start_urls = ['https://play.google.com/store/search?q=facebook']
    
    # Parse from the root URL
    def parse(self, response):
        # Open csv file to delete everything
        f = open('tutorial.csv', 'r+')
        f.truncate(0)
        f.close()
        # Contain all the link of the search results
        app_links = []
        # Get all the urls contain the keywords of the search results
        for res in response.xpath('//*[contains(@href, "facebook")]/@href'):
            app_links.append(res.get())
        # Scrape all the links in the search result 
        for link in app_links:
            if link is not None:
                absolute_link = response.urljoin(link)
                yield scrapy.Request(absolute_link, callback=self.parse_app)
    
    # Parse each app in the search results
    def parse_app(self, response):
        yield {
            'link': response.url,
            'title': response.css('h1.AHFaub span::text').get()
        }
            