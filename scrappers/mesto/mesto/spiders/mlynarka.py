import scrapy
import re
from datetime import date
from decimal import Decimal

from ..items import DonorItem


class MlynarkaSpider(scrapy.Spider):
    """
    TODO:
    """
    name = 'mlynarka'
    start_urls = ['https://ib.fio.cz/ib/transparent?a=2402658875']

    def clean_values(self, data):
        out = {}
        for k, v in data.items():
            out[k] = v.strip() if v is not None else v
        return out

    def parse_date(self, date_str):
        day, month, year = date_str.strip().split('.')
        return str(date(int(year), int(month), int(day)))

    def parse(self, response):
        for item in response.css('table')[1].css('tbody tr'):
            cells = item.css('td')
            data = self.clean_values({
                "date": cells[0].css('::text').get(),
                "amount": cells[1].css('::text').get().replace('CZK', '').replace('\xa0', '').replace(',', '.'),
                "type": cells[2].css('::text').get(),
                "account": cells[3].css('::text').get(),
                "message": cells[4].css('::text').get(),
                "ks": cells[5].css('::text').get(),
                "vs": cells[6].css('::text').get(),
                "ss": cells[7].css('::text').get(),
                "note": cells[8].css('::text').get(),
            })
            data['date'] = self.parse_date(data['date'])
            data['amount'] = str(Decimal(data['amount']))
            yield DonorItem(**data)
