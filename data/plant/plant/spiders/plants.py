from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
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
    name = "plant"
    allowed_domains = ["houseplant411.com"]
    start_urls = get_urls()

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        addresses = hxs.xpath("//div[@id='bodycontent']")
        items = []
        for address in addresses:
            item = PlantItem()
            item["name"] = address.select("div[@class='post']/div[@class='pagebanner']/h2/text()").extract()
            #item["alt_name"] = address.select("div[@class='resultAltName']/text()").extract()
            item["species"] = address.select("div[@class='post']/div[@class='pagebanner']/div[@class='clear resultSpecies']/text()").extract()
            item["key"] = address.select("div[@class='post']/div[@class='contents']/div[@id='tabbedinfo']/div[@class='tabscontain']/div[@class='tabs']/div[@class='post-meta']/div[@class='post-meta-key']/text()").extract()
            item["value"] = address.select("div[@class='post']/div[@class='contents']/div[@id='tabbedinfo']/div[@class='tabscontain']/div[@class='tabs']/div[@class='post-meta']/div[@class='post-meta-value']/text()").extract()

            items.append(item)
        return items
