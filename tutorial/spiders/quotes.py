# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QuoteItem,AuthorItem
from selenium import webdriver
from scrapy import Request
from selenium.webdriver.chrome.options import Options

class QuotesSpider(scrapy.Spider):
	name = 'quotes'
	allowed_domains = ['quotes.toscrape.com']
	base_url='http://quotes.toscrape.com/'

	# start_urls = ['http://http://quotes.toscrape.com/page/1//']

	def __init__(self):
		self.driver=webdriver.PhantomJS()
		# br = webdriver.Chrome()
		# br=	webdriver.PhantomJS()
		#使用chrome无头浏览器
		# chrome_options = Options()
		# chrome_options.add_argument('--headless')
		# chrome_options.add_argument('--disable-gpu')
		# self.driver= webdriver.Chrome(chrome_options=chrome_options)	

	def start_requests(self):
		urls=[
			'http://quotes.toscrape.com',
		]
		headers={
			'Host': 'quotes.toscrape.com',
			'Connection': 'keep-alive',
			'Cache-Control':' max-age=0',
			'Upgrade-Insecure-Requests': 1,
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Referer': 'http://quotes.toscrape.com/page/2/',
			'Accept-Encoding':' gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		}
		for url in urls:
			yield Request(url=url,callback=self.quote_parse,headers=headers)

	def quote_parse(self, response):
		div_list=response.xpath('//div[@class="quote"]')

		#抽取具体quote信息
		for div in div_list:
			quote_item=QuoteItem()
			quote_item['content']=div.xpath('span[@class="text"]/text()').get()
			quote_item['author']=div.xpath('//small[@class="author"]/text()').get()
			quote_item['tags']=div.xpath('//meta/@content').get()
			print(quote_item)
			yield quote_item

			#抽取每个作者详情页链接，并发起请求
			author_url=self.base_url+div.xpath('span//a/@href').get()
			yield scrapy.Request(url=author_url,callback=self.author_parse)

		next_page=response.css('.next a')
		if next_page:
			url=self.base_url+ next_page.attrib['href']
			yield Request(url=url,callback=self.quote_parse)

	def author_parse(self,response):
		author_item=AuthorItem()
		author_item['name']=response.xpath('//h3[@class="author-title"]/text()').get()
		author_item['borndate']=response.xpath('//span[@class="author-born-date"]/text()').get()
		author_item['bornlocation']=response.xpath('//span[@class="author-born-location"]/text()').get()
		author_item['desc']=response.xpath('//div[@class="author-description"]/text()').get()
		# print(author_item)
		yield author_item