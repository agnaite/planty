# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item, Field


class PlantItem(scrapy.Item):
    name = Field()
    #alt_name = Field()
    species = Field()
    key = Field()
    value = Field()
