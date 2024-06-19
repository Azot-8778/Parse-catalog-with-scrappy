import scrapy

class ProductsSpider(scrapy.Spider):
    name = "products_spider"
    allowed_domains = ["order-nn.ru"]
    start_urls = ["https://order-nn.ru/kmo/catalog/5999/"]

    def parse(self, response):
        for product in response.xpath('//div[@class="horizontal-product-item-container"]'):
            name = product.xpath(
                './/div[@class="horizontal-product-item-block_3_2"]/a/span[@itemprop="name"]/text()').get()
            price = product.xpath('.//span[@itemprop="price" and contains(@class, "span-price-number")]/text()').get()
            product_url = product.xpath('.//div[@class="horizontal-product-item-block_3_2"]/a/@href').get()

            # Формируем абсолютный URL для перехода на страницу товара
            product_url = response.urljoin(product_url)

            # Переходим на страницу товара для извлечения описания
            yield scrapy.Request(url=product_url, callback=self.parse_description, meta={'name': name, 'price': price})

        # # Пагинация (если необходимо)
        # next_page = response.xpath("//a[@rel='canonical' and .//i[contains(@class, 'fa-angle-right')]]/@href").get()
        # if next_page:
        #     next_page_url = response.urljoin(next_page)
        #     yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_description(self, response):
        name = response.meta['name']
        price = response.meta['price']
        description = response.xpath('//div[@id="block-description"]/div[@id="for_parse"]/p//text()').getall()
        description = ' '.join(description).strip()

        yield {
            'name': name,
            'price': price,
            'description': description
        }