import scrapy
import os, re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
class GitSpider(CrawlSpider):
    name = "git"
    DOWNLOAD_DELAY = 10.0
    AUTOTHROTTLE_ENABLED = True
    ROBOTSTXT_OBEY = True
    start_urls = ['https://github.com/Taoudi']
    allowed_domains = ['github.com']
    rules = (
        Rule(LinkExtractor(allow=(r'(https://github.com/Taoudi)[^\s]+[\.java]'), deny=(r'.*(blob|commits)')),
            callback='parse_item', follow=True),
    )

    #def start_requests(self):
    
        
        #for url in urls:
        #    yield scrapy.Request(url=url, callback=self.parse_item)
        

    def parse_item(self, response):
        file_url = response.css('.downloadline::attr(href)').get()
        file_url = response.urljoin(file_url)

        filename = 'giturls.txt'
        javafilename = 'javafilesnames.txt'

        if os.path.exists(filename):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not
        f = open(filename,append_write)
        f.write(file_url+'\n')
        f.close()

        
        if re.match(r'^.*\.java$',file_url):
            print(file_url)
            print("----------------------------------------")
            if os.path.exists(javafilename):
                jappend_write = 'a' # append if already exists
            else:
                jappend_write = 'w' # make a new file if not
            
            jf = open(javafilename,jappend_write)
            jf.write(file_url+'\n')
            jf.close()

        

      

        yield {'file_url': file_url}
