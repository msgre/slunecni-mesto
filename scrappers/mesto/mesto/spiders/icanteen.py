import scrapy
import re

from ..items import MenuItem


class ICanteenSpider(scrapy.Spider):
    """
    Scrapper jidelnicku vytvoreneho v systemu iCanteen.

    Pro spravnou funkci je nutne dodat ID jidelnicku, viz parametr canteen_id
    v konstruktoru, nebo parametr -a pokud se vola z CLI:

        scrapy crawl icanteen -a canteen_id=<id>

    Pozor! Scrapper neni prilis obecny, ruzne skoly pouzivaji web iCanteen ruzne,
    tato varianta scraperu byla nastavena na skolu ktera me zajimala.
    """
    name = 'icanteen'

    ALERGENS_RE = re.compile(r'\([ 0-9,]+?\)')
    MULTISPACE_RE = re.compile(r'\s+')

    def __init__(self, canteen_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [f'https://strav.nasejidelna.cz/{canteen_id}/login']

    def clean_lunch(self, lunch):
        meal = lunch.replace('\n', ' ').strip()
        meal = self.ALERGENS_RE.sub('', meal)
        meal = self.MULTISPACE_RE.sub(' ', meal)
        meal = meal.replace(' ,', ',')
        soup, main = meal.split(',', 1)
        main = main.strip()
        return f'{soup.strip()}  \n{main[0].upper() + main[1:]}'

    def parse(self, response):
        for item in response.css('.jidelnicek .jidelnicekDen'):
            date = item.css('.jidelnicekDen .jidelnicekTop')[0].attrib['id'].replace('day-', '')
            human_date = date.split('-')
            human_date = f'{human_date[2].lstrip("0")}.{human_date[1].lstrip("0")}.'
            lunches = item.css('article .column.jidelnicekItem::text')
            if len(lunches) > 0:
                lunch1 = self.clean_lunch(lunches[0].getall()[0])
            else:
                lunch1 = None
            if len(lunches) > 1:
                lunch2 = self.clean_lunch(lunches[1].getall()[0])
            else:
                lunch2 = None
            yield MenuItem(date=date, human_date=human_date, lunch1=lunch1, lunch2=lunch2)
