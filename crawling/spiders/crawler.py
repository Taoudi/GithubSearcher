import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
class GitSpider(CrawlSpider):
    name = "git"
    start_urls = ['https://github.com/Taoudi']
    allowed_domains = ['github.com']
    rules = (
        Rule(LinkExtractor(allow=r'Taoudi/'),
            callback='parse_item', follow=True),
    )

    #def start_requests(self):
    
        
        #for url in urls:
        #    yield scrapy.Request(url=url, callback=self.parse_item)
        

    def parse_item(self, response):
        file_url = response.css('.downloadline::attr(href)').get()
        file_url = response.urljoin(file_url)
        f = open("URLS.txt", "w")
        f.write(str(file_url))
        f.close()

        yield {'file_url': file_url}
