import scrapy
import time
import re
from pymongo import MongoClient

class QuotesSpider(scrapy.Spider):
    name = "net163"
    documentDate = time.strftime("w%y%m%d%H%M",time.localtime())
    client = MongoClient('主机IP', 端口)
    admin = client.admin
    admin.authenticate('数据库授权过的用户名', '密码')
    db = client.w163
    varCollection = db.create_collection(documentDate)

    def start_requests(self):
        allowed_domains = ['163.com']
        urls = [
            'http://news.163.com/',
            'http://war.163.com/',
            'http://news.163.com/photo/',
            'http://news.163.com/air/',
            'http://ent.163.com/',
            'http://ent.163.com/movie/',
            'http://live.ent.163.com/?f=163.homeMint',
            'http://ent.163.com/tv/',
            'http://sports.163.com/',
            'https://hongcai.163.com/?from=pcsy-daohang',
            'http://sports.163.com/nba/',
            'http://sports.163.com/china/',
            'http://money.163.com/',
            'http://money.163.com/stock/',
            'http://money.163.com/fund/',
            'http://biz.163.com/',
            'http://tech.163.com/',
            'http://mobile.163.com/',
            'http://tech.163.com/smart/',
            'http://caipiao.163.com/?from=163',
            'http://fashion.163.com/',
            'http://lady.163.com/',
            'http://edu.163.com/',
            'http://baby.163.com/',
            'http://v.163.com/',
            'http://v.163.com#!zhibohao',
            'http://open.163.com/',
            'http://house.163.com/',
            'http://home.163.com/',
            'http://esf.house.163.com/',
            'http://auto.163.com/',
            'http://auto.163.com/buy/',
            'http://product.auto.163.com/autosearch/',
            'http://jiankang.163.com/',
            'http://jiu.163.com/',
            'http://jiankang.163.com/special/gongkaike/',
            'http://ningbo.news.163.com',
            'http://gov.163.com/',
            'http://tie.163.com/',
            'http://travel.163.com/',
            'http://you.163.com/?from=web_fc_menhu_dhrukou',
            'http://gongyi.163.com/',
            'http://foxue.163.com/',
            'http://dy.163.com/#indexdy',
            'http://art.163.com/',
            'http://news.163.com/shuangchuang',
            'http://art.163.com/uctionlist'
        ]
        for url in urls:
           yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//div[@id="epContentLeft"]/h1/text()').extract_first()
        content = response.xpath('//*[@id="endText"]/*/text()').extract()
        spiderTime = time.strftime("%y/%m%d-%H:%M:%S",time.localtime())
        if title is not None:
            self.varCollection.insert({'spiderTime':spiderTime,'title':title,'content':content})

        shijian = time.strftime("%y/%m%d",time.localtime())
        links = response.xpath("//a[contains(@href,'%s')]/@href" % shijian).extract()
        for href in links:
            yield response.follow(href, callback=self.parse)
