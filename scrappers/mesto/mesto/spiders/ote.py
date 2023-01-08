import scrapy

from ..items import DayPricesItem


class OTESpider(scrapy.Spider):
    """
    Stahne z webu www.ote-cr.cz spotove ceny elektriny pro zadany den.
    """
    name = 'ote'

    def __init__(self, report_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_date = report_date
        self.start_urls = [f'https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date={report_date}']

    def parse(self, response):
        jsonresponse = response.json()
        found = None

        for data in response.json()['data']['dataLine']:
            if data['tooltip'] == 'Cena':
                found = data
                break

        if not found:
            return

        unit = data['title'].split('(')[-1].rstrip(')').strip()
        prices = [item['y'] for item in data['point']]
            
        return DayPricesItem(prices=prices, unit=unit, date=self.report_date)
