import scrapy


class PocasiSpider(scrapy.Spider):
    """
    Stahne JSON data o pocasi z webu yr.no.
    """
    name = 'pocasi'
    start_urls = ['https://api.met.no/weatherapi/locationforecast/2.0/complete?lat=49.4715&lon=17.9715']

    def parse(self, response):
        return response.json()
