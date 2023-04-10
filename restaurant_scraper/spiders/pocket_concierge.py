import scrapy
import pandas as pd
import re

area = "1"
date = "2023-04-23"


class PocketConciergeScraper(scrapy.Spider):
    name = "pocket_concierge"
    start_urls = [f"https://pocket-concierge.jp/en/restaurants?area={area}&date={date}"]

    def parse(self, response):
        for restaurant in response.css("li.col-xl-4"):
            name = restaurant.css("h4.card-title::text").get()
            price = restaurant.css("p.card-text::text").get()
            price = re.sub(r"\D", "", price)

            link = f"https://pocket-concierge.jp{restaurant.css('a.text-restaurant-index::attr(href)').get()}"
            yield scrapy.Request(
                url=link,
                callback=self.parse_restaurant_details,
                meta={"name": name, "price": price, "link": link},
            )
        next_page = response.css(
            "li.pagination-pokeme-side a[rel='next']::attr(href)"
        ).get()
        if next_page is not None:
            yield response.follow(f"https://pocket-concierge.jp{next_page}", self.parse)

    def parse_restaurant_details(self, response):
        name = response.meta["name"]
        price = response.meta["price"]
        link = response.meta["link"]

        tablelog_link = response.css("div.info-item p.info-text a::attr(href)").get()

        yield scrapy.Request(
            url=tablelog_link,
            callback=self.parse_restaurant_tablelog,
            meta={"name": name, "price": price, "link": link},
        )

    def parse_restaurant_tablelog(self, response):
        rating = response.css(
            "#js-header-rating .rdheader-rating__score-val-dtl::text"
        ).get()
        name = response.meta["name"]
        price = response.meta["price"]
        link = response.meta["link"]
        yield {
            "name": name,
            "price": price,
            "rating": rating,
            "link": link,
        }