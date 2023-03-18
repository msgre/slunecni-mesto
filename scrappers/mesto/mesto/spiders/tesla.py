import json
import scrapy

from datetime import datetime
from urllib.parse import quote


class TeslaSpider(scrapy.Spider):
    """
    Vytahne info o skladovych Tesla Model Y dle zadanych parametru.
    """
    name = 'tesla'

    def __init__(self, market='CZ', language='cs', trim='SRRWD', paint='WHITE', interior='PREMIUM_WHITE', wheels='NINETEEN', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.market = 'CZ'
        self.params = {
            "query":{
                "model":"my",
                "condition":"new",
                "options":{
                    "TRIM":[trim],
                    "PAINT":[paint],
                    "INTERIOR":[interior],
                    "WHEELS":[wheels]
                },
                "arrangeby":"Relevance",
                "order":"desc",
                "market":market,
                "language":language,
                "super_region":"north america",
                "lng":17.9664,
                "lat":49.4715,
                "zip":"757 01",
                "range":0
            },
            "offset":0,
            "count":50,
            "outsideOffset":0,
            "outsideSearch":False
        }
        query = quote(json.dumps(self.params))
        self.start_urls = [f'https://www.tesla.com/inventory/api/v1/inventory-results?query={query}']

    def parse(self, response):
        data = response.json()
        if 'approximate' in data['results']:
            results = []
            approx_results = [{
                'TRIM': i['TRIM'],
                'PAINT': i['PAINT'],
                'INTERIOR': i['INTERIOR'],
                'WHEELS': i['WHEELS'],
                'ADL_OPTS': i['ADL_OPTS'],
                'TotalPrice': i['TotalPrice'],
                'City': i['City'],
                'CurrencyCode': i['CurrencyCode'],
                'EtaToCurrent': i['EtaToCurrent'],
                'Year': i['Year'],
            } for i in data['results']['approximate']]
        else:
            results = [{
                'TRIM': i['TRIM'],
                'PAINT': i['PAINT'],
                'INTERIOR': i['INTERIOR'],
                'WHEELS': i['WHEELS'],
                'ADL_OPTS': i['ADL_OPTS'],
                'TotalPrice': i['TotalPrice'],
                'City': i['City'],
                'CurrencyCode': i['CurrencyCode'],
                'EtaToCurrent': i['EtaToCurrent'],
                'Year': i['Year'],
            } for i in data['results']]
            approx_results = []
        return {
            "count": data["total_matches_found"],
            "results": results,
            "approx_count": len(approx_results),
            "approx_results": approx_results,
            "options": self.params['query']['options'],
            "datetime": datetime.now(),
        }
