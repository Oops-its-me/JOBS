# -*- coding: utf-8 -*-


from scrapy import Spider
from scrapy import Request

class JobSpider(Spider):
    name = 'job'
    allowed_domains = ['craigslist.org']
    start_urls = ['http://newyork.craigslist.org/search/egr/']

    def parse(self, response):

        job_urls = response.xpath('//*[@class="result-info"]/a/@href').extract()

        for rel_url in job_urls:
            abs_url = response.urljoin(rel_url)
            yield Request(abs_url,callback=self.parse_job,meta={'URL':abs_url})


        next_page = response.xpath('//*[@class="button next"]/@href').extract_first()
        next_page_url = response.urljoin(next_page)
        yield Request(next_page_url,callback=self.parse)

    def parse_job(self, response):

        title = response.xpath('//*[@id="titletextonly"]/text()').extract_first()
        location_temp = response.xpath('//*[@class="postingtitletext"]/small/text()').extract_first()
        location = location_temp.strip("' ', '(', ')'")
        compensation = response.xpath('//p[@class="attrgroup"]/span[1]/b/text()').extract()
        job_type = response.xpath('//p[@class="attrgroup"]/span[2]/b/text()').extract()
        url = response.meta.get('URL')

        yield {'Title': title,
               'Location': location,
               'Compensation': compensation,
               'Job type': job_type,
               'Link': url}