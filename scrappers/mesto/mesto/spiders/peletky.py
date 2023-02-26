from datetime import date

import scrapy


class WalderaSpider(scrapy.Spider):
    """
    Stahne z webu www.waldera.cz informaci o cene peletek.
    """
    name = 'waldera'

    def __init__(self, quantity=3, zipid=72279, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quantity = quantity * 1050
        self.zipid = zipid
        self.start_urls = [
	        f'https://www.waldera.cz/sys-ajax/loadTransports/?params[zipId]={zipid}&params[productId]=5',
        ]

    def parse(self, response):
        """
        Vyzobne transportationID, ktere se furt meni.
        """
        transportationid = response.css('input[name="doprava"]').attrib['value']
        url = f'https://www.waldera.cz/sys-ajax/getProductPrice/?params[productID]=5&params[quantity]={self.quantity}%2C00&params[transportationID]={transportationid}&params[zipId]={self.zipid}'
        page  = response.urljoin(url)
        yield scrapy.Request(page, callback=self.parse_product)

    def parse_product(self, response):
        """
        Vyparsuje cenu paletek.
        """
        price = response.json()["data"]["price"].replace('&nbsp;', '').replace('Kč', '').replace(',', '.').strip()
        quantity = response.json()["data"]["quantity"].replace('&nbsp;', '').replace(',', '.').strip()
        yield {"price": float(price), "quantity": int(float(quantity)), "date": str(date.today())}


class BiomacSpider(scrapy.Spider):
    """
    Stahne z webu eshop.biomac.cz informaci o cene peletek.
    """
    name = 'biomac'
    paleta_hmotnost = 1050  # NOTE: 1050 kg na palete je i primo v URL, nemusim to znovu hledat na strance
    paleta_cena = 250  # NOTE: maji to v popisu, neoveruju ze to porad sedi

    def __init__(self, quantity=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quantity = quantity
        self.start_urls = [f'https://eshop.biomac.cz/drevene-pelety-top-a1-paleta-1050kg-g8901.html']

    def parse(self, response):
        price = response.selector.css('table.goods-detail-price tr:nth-child(1) td:nth-child(2)::text').get()
        price = price.replace('Kč', '').replace(' ', '').strip()
        price = (float(price) + self.paleta_cena) * self.quantity 
        return {'price': price, "quantity": self.paleta_hmotnost * self.quantity, "date": str(date.today())}
