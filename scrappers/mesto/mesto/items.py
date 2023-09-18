import scrapy


class DayPricesItem(scrapy.Item):
    """
    Ceny elektriny na spotovem trhu pro konkretni den.

    Polozka prices je seznam cen, index reprezentuje hodinu
    (napr na indexu 0 je cena platna od 0:00 do 0:59).
    """
    date = scrapy.Field()
    prices = scrapy.Field()
    unit = scrapy.Field()


class MenuItem(scrapy.Item):
    """
    Zaznam o obedovem menu pro konkretni den.
    
    Poznamka: skola ktera me zajimala mela v nabidce 2 ruzne obedy pro kazdy den,
    jine skoly mohou mit jidelnicky sestaveny jinak.
    """
    date = scrapy.Field()
    human_date = scrapy.Field()
    lunch1 = scrapy.Field()
    lunch2 = scrapy.Field()


class DonorItem(scrapy.Item):
    date = scrapy.Field()
    amount = scrapy.Field()
    type = scrapy.Field()
    account = scrapy.Field()
    message = scrapy.Field()
    ks = scrapy.Field()
    vs = scrapy.Field()
    ss = scrapy.Field()
    note = scrapy.Field()
