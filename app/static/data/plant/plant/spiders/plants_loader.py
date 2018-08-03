from scrapy.loader import ItemLoader
from scrapy.spiders import BaseSpider
from plant.items import PlantItem
import json


def get_urls():
    """Parse a json file to pull out all the urls and save them in a list"""

    urls = []
    with open('urls.json') as data_file:
        data = json.load(data_file)
    # takes each item in dictionary, gets the link from key 'url' and
    # appends url to list urls
    for item in data:
        urls.append(item['url'][0])

    return urls


class MySpider(BaseSpider):
    name = "plant_load"
    allowed_domains = ["houseplant411.com"]
    start_urls = get_urls()

    def parse(self, response):
        l = ItemLoader(item=PlantItem(), response=response)

        l.add_xpath('name', "//div[@id='bodycontent']/div[@class='post']/div[@class='pagebanner']/h2/text()")
        l.add_xpath('species', "//div[@id='bodycontent']/div[@class='post']/div[@class='pagebanner']/div[@class='clear resultSpecies']/text()")
        l.add_xpath('key', "//div[@id='bodycontent']/div[@class='post']/div[@class='contents']/div[@id='tabbedinfo']/div[@class='tabscontain']/div[@class='tabs']/div[@class='post-meta']/div[@class='post-meta-key']/text()")
        l.add_xpath('value', "//div[@id='bodycontent']/div[@class='post']/div[@class='contents']/div[@id='tabbedinfo']/div[@class='tabscontain']/div[@class='tabs']/div[@class='post-meta']/div[@class='post-meta-value']/child::node()")
        # l.add_xpath('value', "//div[@id='bodycontent']/div[@class='post']/div[@class='contents']/div[@id='tabbedinfo']/div[@class='tabscontain']/div[@class='tabs']/div[@class='post-meta']/div[@class='post-meta-value']/a/text()")

        return l.load_item()
