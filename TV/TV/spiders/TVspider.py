#-*-coding:utf8-*-
from scrapy.contrib.spiders import CrawlSpider
import pdb
from TV.items import TvItem
# import scrapy

class TVSpider(CrawlSpider):
    """docstring for TVSpider"""

    name = 'TVSpider'
    allowed_domains = ["TVSpider"]
    start_urls = ["http://www.panda.tv/cate/hearthstone",
    "http://www.douyu.com/directory/game/How"]

    def parse(self,response):
        item = TvItem()
        if response.url[:20] == 'http://www.panda.tv/':
            item['source'] = self._pandaResponse(response)
        elif response.url[:20] == 'http://www.douyu.com':
            item['source'] = self._douyuResponse(response)
        # pdb.set_trace()
        return item


    def _douyuResponse(self,response):
        source = response.xpath('//*[@id="live-list-contentbox"]/li')
        sourceList = []
        for src in source:
            roomid = src.xpath('@data-rid').extract()[0]
            number = src.xpath('a/div/p/span[2]/text()').extract()[0]
            title = src.xpath('a/div/div/h3/text()').extract()[0]
            name = src.xpath('a/div/p/span[1]/text()').extract()[0]
            if number.find(u'\u4e07') > 0:
                number = str(eval(number[:-1])*10000).decode('utf-8')
            sourceList.append((name,title,roomid,number))
        return sourceList

    def _pandaResponse(self,response):
        source = response.xpath('//*[@id="sortdetail-container"]/li/a')
        sourceList = []
        for src in source:
            roomid = src.xpath('@data-id').extract()[0]
            number = src.xpath('div[3]/span[2]/text()').extract()[0]
            title = src.xpath('div[2]/text()').extract()[0]
            name = src.xpath('div[3]/span[1]/text()').extract()[0]
            sourceList.append((name,title,roomid,number))
        return sourceList
