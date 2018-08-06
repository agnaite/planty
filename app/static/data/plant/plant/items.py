# -*- coding: utf-8 -*-
import scrapy
from scrapy.item import Item, Field


class PlantItem(scrapy.Item):
    name = Field()
    species = Field()
    title = Field()
    description = Field()
