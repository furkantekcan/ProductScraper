from typing import Iterable

import scrapy
import os
import xml.etree.ElementTree as ET

from scrapy import Request

from ..items import ProductscraperItem


class ProductScraper(scrapy.Spider):
    name = 'product_scraper'
    start_urls = ['file:///C:/Users/furka/OneDrive/Belgeler/PythonProject/ProductScraper/lonca-sample.xml']

    def parse(self, response):
        items = ProductscraperItem()

        # all_div_quotes = response.css('div.quote')
        #
        # for quote in all_div_quotes:
        #     title = quote.css('span.text::text').extract()
        #     author = quote.css('.author::text').extract()
        #
        #     items['title'] = title
        #     items['author'] = author
        #
        #     yield items
        root = ET.fromstring(response.body)

        # Iterate over each Product element
        for product in root.findall('Product'):
            # Extract data from Product attributes and sub-elements
            items['ProductId'] = product.get('ProductId')
            items['Name'] = product.get('Name')
            items['Price'] = next((detail.get('Value') for detail in product.find('ProductDetails').findall('ProductDetail') if detail.get('Name') == 'Price'), None)

            yield items
