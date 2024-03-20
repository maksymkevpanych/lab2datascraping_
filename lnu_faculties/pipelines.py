# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LnuFacultiesPipeline:
    def process_item(self, item, spider):
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
    def open_spider(self, spider):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='12345',
                password='12345',
                database='lab3datascraping'
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print("Connected to MySQL database")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def close_spider(self, spider):
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("MySQL connection closed")

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""
                INSERT INTO faculty_data (faculty_name, faculty_link, news_title, news_link)
                VALUES (%s, %s, %s, %s)
            """, (
                item.get('faculty_name'),
                item.get('faculty_link'),
                item.get('news_title'),
                item.get('news_link')
            ))
            self.conn.commit()
            print("Item added to MySQL database")
        except Error as e:
            print("Error while inserting data into MySQL", e)
        return item
