import csv

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RestaurantScraperPipeline:
    def process_item(self, item, spider):
        return item


class CsvPipeline:
    def open_spider(self, spider):
        self.file = open("output.csv", mode="w", encoding="utf-8", newline="")
        self.writer = csv.writer(self.file)
        self.writer.writerow(["name", "price", "rating", "link"])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(
            [item["name"], item["price"], item["rating"], item["link"]]
        )
        return item