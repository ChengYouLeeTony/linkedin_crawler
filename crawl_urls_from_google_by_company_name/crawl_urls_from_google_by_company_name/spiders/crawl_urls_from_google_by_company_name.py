from crawl_urls_from_google_by_company_name.items import CrawlUrlsFromGoogleByCompanyNameItem
import scrapy
import time

class PTTSpider(scrapy.Spider):
    name = 'linkedin_from_google'
    def __init__(self, company=None, *args, **kwargs):
      self.allowed_domains = ['google.com']
      self.start_urls = ["https://www.google.com/search?q=%s+site:linkedin.com" % company]
      self.url = self.start_urls[0]
      self.count = 0

    def parse(self, response):
      while self.count <= 10:
        time.sleep(1)
        yield scrapy.Request (self.url, callback=self.parse_url)

    def parse_url(self, response):
      item = CrawlUrlsFromGoogleByCompanyNameItem()
      pattern = r'q=.*?&'
      target = response.xpath('//a[contains(@href, "/url?q=https://tw.linkedin.com/in/")]').re(pattern)
      next_page_url = response.xpath('//a[@aria-label="下一頁"]//@href').extract_first()
      self.url = 'https://www.google.com' + next_page_url
      for url in target:
        try:
          item['url'] = url[2:-1]
          self.count += 1
          yield item
        except IndexError:
          pass
        continue