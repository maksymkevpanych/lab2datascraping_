import scrapy

class FacultyItem(scrapy.Item):
    faculty_name = scrapy.Field()
    faculty_link = scrapy.Field()
    news_title = scrapy.Field()
    news_link = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
