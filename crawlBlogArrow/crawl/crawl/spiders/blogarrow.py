import scrapy
from scrapy import Spider
from crawl.items import CrawlItem

class CrawlerSpider(Spider):
    name = "crawler"
    allowed_domains = ["blog.arrow-tech.vn"]
    start_urls = [
        "https://blog.arrow-tech.vn/detect-labels-faces-and-landmarks-in-images-with-the-cloud-vision-api/",
    ]
    
    def parse(self, response):

        item = CrawlItem()
        item['title'] = response.xpath('//h1[@class="post-title u-fontSizeLargest u-md-fontSizeLarger"]/text()').extract()[0].strip()    
        thumb_link = "https://blog.arrow-tech.vn" + response.xpath('//img[@class="post-img u-block u-marginAuto"]/@src').extract()[0].strip()   
        item['thumb'] = thumb_link.split('/')[-1]
        yield scrapy.Request(thumb_link,callback=self.parse_img)
        item['author'] =  response.xpath('//a[@class="link link--underline u-fontWeightMedium u-textColorDarker"]/text()').extract()[0].strip() 
        item['content'] =  response.xpath('//div[@class="post-inner js-post-content"]').extract()[0].strip() 
        yield item


    def parse_img(self, response):
        with open("img/%s" % response.url.split('/')[-1], 'wb') as f:
            f.write(response.body)
    

    