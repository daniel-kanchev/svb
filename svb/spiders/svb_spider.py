import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from svb.items import Article


class Svb_spiderSpider(scrapy.Spider):
    name = 'svb_spider'
    start_urls = ['https://www.svb.com/news/company-news']

    def parse(self, response):
        links = response.xpath('//a[@class="grid__col list-items__more"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get().strip()
        date = response.xpath('//span[@itemprop="datePublished"]/text()').get().strip()
        try:
            date = datetime.strptime(date, '%B %d, %Y')
        except:
            return
        date = date.strftime('%Y/%m/%d')
        content = response.xpath('//div[@class="C06 "]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
