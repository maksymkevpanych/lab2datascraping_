# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handli
# ng different item types with a single interface
import scrapy
import uuid
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import json
class LnuFacultiesPipeline:
    def process_item(self, item, spider):
        return item

class FacultyImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if 'image_urls' in item:
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if image_paths:
            item['images'] = image_paths
        return item    
class CapitalToOrdinaryPipeline:
    def process_item(self, item, spider):
        for field, value in item.items():
            if isinstance(value, str):
                item[field] = ''.join(c.lower() if c.isupper() else c for c in value)
        return item
import mysql.connector
from mysql.connector import Error

class MySQLPipeline:
    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_password):
        self.mysql_host = 'localhost'
        self.mysql_db = 'lab3datascraping   '
        self.mysql_user = '12345'
        self.mysql_password = '12345'
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_host=crawler.settings.get('MYSQL_HOST'),
            mysql_db=crawler.settings.get('MYSQL_DATABASE'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD')
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=self.mysql_host,
            database=self.mysql_db,
            user=self.mysql_user,
            password=self.mysql_password
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # Generate a unique identifier for the item
        item_id = uuid.uuid4().hex

        # Assuming `item` is a dictionary containing your scraped data
        columns = ', '.join(item.keys())
        placeholders = ', '.join(['%s'] * len(item))

        # Adjust values to include the generated item_id
        values = [item_id]
        for key, value in item.items():
            if key == 'id':  # Skip 'id' field if present
                continue
            if isinstance(value, list):
                value = json.dumps(value)
            values.append(value)

        # Adjust the SQL query accordingly
        sql = f"INSERT INTO {'faculty_data'} (id, {columns}) VALUES (%s, {placeholders})"
        self.cursor.execute(sql, values)
        
        # Save image URLs if available
        if 'image_urls' in item:
            image_urls = item['image_urls']
            for image_url in image_urls:
                self.cursor.execute("INSERT INTO faculty_data (image_urls, item_id) VALUES (%s, %s)", (image_url, item_id))
        self.conn.commit()
        return item