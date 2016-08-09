# scrapy crawl plant -o with_urls.json

from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from plant.items import PlantItem
from pprint import pprint
import json
import re


from itertools import izip_longest

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

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

        # TODO get the plant name

        keys = response.xpath("//div[@class='post-meta-key']")
        values = response.xpath("//div[@class='post-meta-value']")

        response.select("//div[@class='post']/div[@class='pagebanner']/h2/text()").extract()

        assert len(keys) == len(values)

        results = []

        for key, value in zip(keys, values):

            foo = value.xpath('.//text()').extract()

            bar = [foo[0]]
            for z in grouper(3, foo[1:-1]):
                bar.append(z[0])


            key_title = key.xpath('.//text()').extract()[0]

            result = { response.title: { str(key_title): '\n'.join(bar) } }
            print(result)
            print('-'*80)
            results.append(result)

        return results
