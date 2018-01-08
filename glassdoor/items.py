# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GlassdoorInterviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company = scrapy.Field()
    job_title = scrapy.Field()
    review_date = scrapy.Field()
    offer_status = scrapy.Field()
    application_proccess = scrapy.Field()
    interview_experience = scrapy.Field()
    interview_difficulty = scrapy.Field()
    interview_description = scrapy.Field()
    interview_questions = scrapy.Field()
