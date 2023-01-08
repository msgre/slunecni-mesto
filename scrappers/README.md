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

Data taham s pomoci helper scriptu cron.sh:

```
#!/bin/bash

DATETIME=`/bin/date +%Y-%m-%dT%H:%M:%S`
TODAY=`/bin/date +%Y-%m-%d`
TOMORROW=`/bin/date -d "1 day" "+%Y-%m-%d"`

case "$1" in
    obedy)
	/usr/bin/docker run --rm -v /var/www/html/obedy:/output msgre/scrappers scrapy crawl icanteen -a canteen_id=<id> -L ERROR -O /output/obedy-${TODAY}.json:json
	ln -sf /var/www/html/obedy/obedy-${TODAY}.json /var/www/html/obedy/obedy-latest.json
        ;;
    ote)
	/usr/bin/docker run --rm -v /var/www/html/ote:/output msgre/scrappers scrapy crawl ote -a report_date=${TOMORROW} -L ERROR -O /output/ote-${DATETIME}.json:json
	ln -sf /var/www/html/ote/ote-${DATETIME}.json /var/www/html/ote/ote-latest.json
        ;;
    cnb)
	# kurzy CNB se vyhlasuji po 14:30 a plati aktualni den (a pripadnou nasledjujici so+ne ci statni svatek)
	/usr/bin/docker run --rm -v /var/www/html/cnb:/output msgre/scrappers scrapy crawl cnb -a rate_date=${TODAY} -L ERROR -O /output/cnb-${TODAY}.json:json
	ln -sf /var/www/html/cnb/cnb-${TODAY}.json /var/www/html/cnb/cnb-latest.json
        ;;
    peletky)
	/usr/bin/docker run --rm -v /var/www/html/peletky:/output msgre/scrappers scrapy crawl waldera -L ERROR -O /output/peletky-waldera-${TODAY}.json:json
	/usr/bin/docker run --rm -v /var/www/html/peletky:/output msgre/scrappers scrapy crawl biomac -L ERROR -O /output/peletky-biomac-${TODAY}.json:json
	ln -sf /var/www/html/peletky/peletky-waldera-${TODAY}.json /var/www/html/peletky/peletky-waldera-latest.json
	ln -sf /var/www/html/peletky/peletky-biomac-${TODAY}.json /var/www/html/peletky/peletky-biomac-latest.json
        ;;
    *)
        echo "Neznamy parametr"
        ;;
esac
```

Napr. data o spotovych cenach elektriny vytahnu s pomoci `./cron.sh ote`.

Na cronjobu pak mam nastavene konkretni casy:

```
1 0 * * 1-5,7 /path/cron.sh obedy
2 0 * * * /path/cron.sh ote
0 15 * * 1-5 /path/cron.sh cnb
3 0 * * 1,3 /path/cron.sh peletky
```
