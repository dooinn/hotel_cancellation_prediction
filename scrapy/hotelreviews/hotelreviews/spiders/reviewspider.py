import scrapy


class ReviewspiderSpider(scrapy.Spider):
    name = "reviewspider"
    allowed_domains = ["www.booking.com"]
    start_urls = ["https://www.booking.com/hotel/pt/lisbon-city.en-gb.html?aid=311984"]

    def parse(self, response):
        pass
