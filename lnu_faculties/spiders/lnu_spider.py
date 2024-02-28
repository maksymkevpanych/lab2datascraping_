import scrapy


class LnuSpider(scrapy.Spider):
    name = 'lnu'
    start_urls = ['https://lnu.edu.ua/about/faculties/']

    def parse(self, response):
        
        for faculty in response.css('ul.structural-units > li'):
            yield {
                'faculty_name': faculty.css('a::text').get(),
                'faculty_link': faculty.css('a::attr(href)').get()
            }
