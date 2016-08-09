from scrapy.spiders import BaseSpider
from scrapy.selector import HtmlXPathSelector
from plant.items import PlantItem
import json

# from HTMLParser import HTMLParser


# class MLStripper(HTMLParser):
#     def __init__(self):
#         self.reset()
#         self.fed = []

#     def handle_data(self, d):
#         self.fed.append(d)

#     def get_data(self):
#         return ''.join(self.fed)


# def strip_tags(html):
#     s = MLStripper()
#     s.feed(html)
#     return s.get_data()


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
            # item["name"] = address.select("div[@class='post']/div[@class='pagebanner']/h2/text()").extract()
            # item["species"] = address.select("div[@class='post']/div[@class='pagebanner']/div[@class='clear resultSpecies']/text()").extract()
            # item["title"] = address.select("div[@class='post']/div[@class='contents']/div[@id='tabbedinfo']/div[@class='tabscontain']/div[@class='tabs']/div[@class='post-meta']/div[@class='post-meta-key']/text()").extract()
            item["description"] = address.select("div[@class='post']/div[@class='contents']/div[@id='tabbedinfo']/div[@class='tabscontain']/div[@class='tabs']/div[@class='post-meta']/div[@class='post-meta-value']/child::node()").extract()   

            d = item["description"]
            print("-"*80)
            print('{} {}'.format(type(item["description"]), len(item["description"])))
            print(item["description"])
            print("-"*80)

            # my_whole_paragraph = []

            # for node in my_nodes:
            #     some_text = node.select('text()').extract()
            #     my_whole_paragraph.append(some_text)
            #     some_links = node.select('a/text()').extract()
            #     my_whole_paragraph.append(some_links)
            #     some_spans = node.select('span/text()').extract()
            #     my_whole_paragraph.append(some_spans)
                # if some_text:
                #     my_whole_paragraph.append(some_text)
                # else:
                #     my_whole_paragraph.append(node.select("a/text()").extract())

            # item["description"] = my_whole_paragraph

            items.append(item)

        return items
