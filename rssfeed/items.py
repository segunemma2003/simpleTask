# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RssfeedItem(scrapy.Item):
    title = scrapy.Field()
    image_url = scrapy.Field()
    text = scrapy.Field()
