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
        params = {
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
        breakpoint()
        query = quote(json.dumps(params))
        self.start_urls = [f'https://www.tesla.com/inventory/api/v1/inventory-results?query={query}']

    def parse(self, response):
        return {
            "count": response.json()["total_matches_found"],
            "market": self.market,
            "datetime": datetime.now(),
        }
