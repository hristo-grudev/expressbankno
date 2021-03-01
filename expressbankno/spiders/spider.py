import scrapy

from scrapy.loader import ItemLoader
from ..items import ExpressbanknoItem
from itemloaders.processors import TakeFirst


class ExpressbanknoSpider(scrapy.Spider):
	name = 'expressbankno'
	start_urls = ['https://www.expressbank.no/blogg/']

	def parse(self, response):
		post_links = response.xpath('//a[contains(@class, "post-image")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="grid-col-3of4"]//text()[normalize-space() and not(ancestor::h1 | ancestor::div[@class="meta-data"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="meta-data"]/text()[normalize-space()]').get()

		item = ItemLoader(item=ExpressbanknoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
