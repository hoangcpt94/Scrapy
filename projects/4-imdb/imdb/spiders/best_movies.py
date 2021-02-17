# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']

    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc', headers={
            "User-Agent": self.user_agent
            })

    # extract or not extract the link in rules
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='lister-item-image float-left']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[1]"), process_request='set_user_agent')
    )

    # Add spider argument if use scrapy version 2.0+
    # def sef_user_agent(self, request, spider):
    def set_user_agent(self, request):
        request.headers['user-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "title": response.xpath("//div[@class='title_wrapper']/h1/text()").get(),
            "year": response.xpath("//span[@id='titleYear']/a/text()").get(),
            "duration": response.xpath("normalize-space((//time)[1]/text())").get(),
            "genre": response.xpath("//div[@class='subtext']/a[1]/text()").get(),
            "rating": response.xpath("//span[@itemprop='ratingValue']/text()").get(),
            "moving_url": response.url,
            "user-agent": response.request.headers['User-Agent']
        }
