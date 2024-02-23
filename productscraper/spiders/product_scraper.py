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
        root = ET.fromstring(response.body)

        # Iterate over each Product element
        for product in root.findall('Product'):
            # Extract data from Product attributes and sub-elements
            items['id'] = product.get('ProductId')
            items['stock_code'] = product.get('Name')  # Assuming 'Name' contains the stock code
            items['color'] = [image.get('Path') for image in product.find('Images').findall('Image')]
            discounted_price_str = next(
                (detail.get('Value') for detail in product.find('ProductDetails').findall('ProductDetail') if
                 detail.get('Name') == 'DiscountedPrice'), '')
            # Replace comma with dot before converting to float
            discounted_price_str = discounted_price_str.replace(',', '.')
            items['discounted_price'] = float(discounted_price_str) if discounted_price_str else 0
            items['images'] = [image.get('Path') for image in product.find('Images').findall('Image')]
            items['is_discounted'] = float(items['discounted_price']) > 0
            items['name'] = product.get('Name').capitalize()
            items['price'] = next(
                (detail.get('Value') for detail in product.find('ProductDetails').findall('ProductDetail') if
                 detail.get('Name') == 'Price'), 0)
            items['price_unit'] = 'USD'  # Assuming price is in USD
            items['product_type'] = next(
                (detail.get('Value') for detail in product.find('ProductDetails').findall('ProductDetail') if
                 detail.get('Name') == 'ProductType'), '')
            items['quantity'] = int(next(
                (detail.get('Value') for detail in product.find('ProductDetails').findall('ProductDetail') if
                 detail.get('Name') == 'Quantity'), 0))
            items['sample_size'] = ''  # Sample size not available in the XML
            items['series'] = next(
                (detail.get('Value') for detail in product.find('ProductDetails').findall('ProductDetail') if
                 detail.get('Name') == 'Series'), '')
            items['status'] = 'Active'

            yield items
