Scrapery (pro me) zajimavych dat z tech internetu:

* obedy na Jindrove skole
* spotove ceny vykupu elektricke energie
* kurz EUR
* ceny peletek

## Setup

```bash
docker build . -t msgre/scrappers
```

## Spusteni

Obedy:

```bash
docker run -ti --rm -v $PWD:/app msgre/scrappers scrapy crawl icanteen -L ERROR -a canteen_id=<id> -o -:json
```

Spotove ceny elektriny:

```bash
docker run -ti --rm -v $PWD:/app msgre/scrappers scrapy crawl ote -a report_date=2023-01-08 -L ERROR -o -:json
```

Kurz EUR:

```bash
docker run -ti --rm -v $PWD:/app msgre/scrappers scrapy crawl cnb -a rate_date=2023-01-08 -L ERROR -o -:json
```

Peletky:

```bash
docker run -ti --rm -v $PWD:/app msgre/scrappers scrapy crawl waldera -L ERROR -o -:json
docker run -ti --rm -v $PWD:/app msgre/scrappers scrapy crawl biomac -L ERROR -o -:json
```

## Cron

```
TODO:
```
