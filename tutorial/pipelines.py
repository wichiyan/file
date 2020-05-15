# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from tutorial.items import QuoteItem,AuthorItem
import json
class TutorialPipeline:

	#主要是对作者信息数据进行加工处理
	def process_item(self, item, spider):
		if isinstance(item,AuthorItem):
			item['name']=item['name'].replace('\n','').strip()
			item['bornlocation']=item['bornlocation'].replace('in','').strip()
			item['desc']=item['desc'].replace('\n','').strip()
		return item



class FianlePipeline:
	def open_spider(self,spider):
		self.file_quote=open('quotes.json','w')
		self.file_author=open('author.json','w')

	def process_item(self, item, spider):
		if isinstance(item,QuoteItem):
			content=json.dumps(dict(item),ensure_ascii=False)+'\n'
			self.file_quote.write(content)

		elif isinstance(item,AuthorItem):
			content=json.dumps(dict(item),ensure_ascii=False)+'\n'
			self.file_author.write(content)			
		return item


	def close_spider(self,spider):
		self.file_quote.close()
		self.file_author.close()	