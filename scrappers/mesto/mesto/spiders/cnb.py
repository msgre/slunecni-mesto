from datetime import date

import scrapy


class CNBSpider(scrapy.Spider):
    """
    Stahne z webu www.cnb.cz kurz EUR pro dany den.
    """
    name = 'cnb'

    def __init__(self, rate_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not rate_date:
            d = date.today()
            self.utc_date = str(d)
            self.date = d.strftime('%d.%m.%Y')
        elif '-' in rate_date:
            self.utc_date = rate_date
            parts = rate_date.split('-')
            self.date = f'{parts[2]}.{parts[1]}.{parts[0]}'
        else:
            self.date = rate_date
            parts = rate_date.split('.')
            self.utc_date = f'{parts[2]}-{parts[1]}-{parts[0]}'
        self.start_urls = [f'https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/index.html?date={self.date}']

    def parse(self, response):
        price = response.selector.css('table td:contains("EUR") + td::text').get()
        price = price.replace(',', '.').strip()
        yield {'eur': float(price), "date": self.utc_date}
