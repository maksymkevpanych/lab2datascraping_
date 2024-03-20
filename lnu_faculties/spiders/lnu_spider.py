import scrapy
from lnu_faculties.items import FacultyItem

class LnuSpider(scrapy.Spider):
    name = 'lnu'
    start_urls = ['https://lnu.edu.ua/about/faculties/']

    def parse(self, response):
        for faculty in response.css('ul.structural-units > li'):
            faculty_item = FacultyItem()
            faculty_item['faculty_name'] = faculty.css('a::text').get()
            faculty_item['faculty_link'] = faculty.css('a::attr(href)').get()

            yield scrapy.Request(faculty_item['faculty_link'], callback=self.parse_faculty, meta={'faculty_item': faculty_item})

    def parse_faculty(self, response):
        faculty_item = response.meta['faculty_item']
        image_urls = response.css('div.image::attr(style)').re_first(r"url\((.*?)\)")
        if image_urls:
            faculty_item['image_urls'] = [image_urls]
        for news_section in response.css('section.news'):
            news_items = news_section.css('h5 a')
            for news_item in news_items:
                faculty_item['news_title'] = news_item.css('::text').get()
                faculty_item['news_link'] = news_item.css('::attr(href)').get()

                yield faculty_item

    def close(self, reason):
        self.logger.info('Spider closed: %s', reason)
