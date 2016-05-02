# import the necessary packages
from timecoverspider.items import MagazineCover
import datetime
import scrapy

class CoverSpider(scrapy.Spider):
    # name in the shell
	name = "timecover"

	start_urls = ["http://content.time.com/time/covers/0,16641,20140310,00.html"]

	def _parse(self, response):
		# let's only gather Time U.S. magazine covers
		url = response.css("div.refineCol ul li").xpath("a[contains(., 'TIME U.S.')]")
		yield scrapy.Request(url.xpath("@href").extract_first(), self.parse_covers)

	def parse_page(self, response):
            pass
        # loop over all cover link elements that link off to the large
		# cover of the magazine and yield a request to grab the cove
		# data and image

        # for href in response.xpath("//a[contains(., 'Large Cover')]"):
		# 	yield scrapy.Request(href.xpath("@href").extract_first(),
        #                          self.parse_covers)

        # next = response.css("div.pages").xpath("a[contains(., 'Next')]")
        # yield scrapy.Request(next.xpath("@href").extract_first(), self.parse_page)

	def parse(self, response):
		# grab the URL of the cover image
		img = response.css(".art-cover-photo figure a img").xpath("@src")
		imageURL = img.extract_first()

		# grab the title and publication date of the current issue
		title = response.css(".content-main-aside h1::text").extract_first()
		year = response.css(".content-main-aside h1 time a::text").extract_first()
		month = response.css(".content-main-aside h1 time::text").extract_first()[:-2]

		# parse the date
		date = "{} {}".format(month, year).replace(".", "")
		d = datetime.datetime.strptime(date, "%b %d %Y")
		pub = "{}-{}-{}".format(d.year, str(d.month).zfill(2), str(d.day).zfill(2))

		# yield the result
		yield MagazineCover(title=title, pubDate=pub, file_urls=[imageURL])
