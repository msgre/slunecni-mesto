"""
"""

import arrow
import requests
import feedparser
from datetime import date
from bs4 import BeautifulSoup

from flask import Flask
from flask import render_template

app = Flask(__name__)

MONTHS = {
    1: 'ledna',
    2: 'února',
    3: 'března',
    4: 'dubna',
    5: 'května',
    6: 'června',
    7: 'července',
    8: 'srpna',
    9: 'září',
    10: 'října',
    11: 'listopadu',
    12: 'prosince',
}

WEEKDAYS = {
    1: 'Pondělí',
    2: 'Úterý',
    3: 'Středa',
    4: 'Čtvrtek',
    5: 'Pátek',
    6: 'Sobota',
    7: 'Neděle',
}

KROUZKY = {
    2: [
        {
            'od': '16:20',
            'do': '18:20',
            'co': 'Zlaté šípy',
        },
    ],
    3: [
        {
            'od': '17:10',
            'do': '17:55',
            'co': 'Kytara',
        },
        {
            'od': '18:00',
            'do': '18:45',
            'co': 'Skupina',
        },
    ],
}

ROZVRH = {
    1: [
        {
            'hodina': 1,
            'od': '8:00',
            'do': '8:45',
            'predmet': 'Př',
        },
        {
            'hodina': 2,
            'od': '8:55',
            'do': '9:40',
            'predmet': 'Z',
        },
        {
            'hodina': 3,
            'od': '10:00',
            'do': '10:45',
            'predmet': 'ČJ',
        },
        {
            'hodina': 4,
            'od': '10:55',
            'do': '11:40',
            'predmet': 'Hv',
        },
        {
            'hodina': 5,
            'od': '11:50',
            'do': '12:35',
            'predmet': 'Aj',
        },
        {
            'hodina': 6,
            'od': '12:45',
            'do': '13:30',
            'predmet': 'M',
        },
        {
            'hodina': 7,
            'od': '14:00',
            'do': '14:45',
            'predmet': 'INV',
        },
    ],
    2: [
        {
            'hodina': 1,
            'od': '8:00',
            'do': '8:45',
            'predmet': 'M',
        },
        {
            'hodina': 2,
            'od': '8:55',
            'do': '9:40',
            'predmet': 'D',
        },
        {
            'hodina': 3,
            'od': '10:00',
            'do': '10:45',
            'predmet': 'Aj',
        },
        {
            'hodina': 4,
            'od': '10:55',
            'do': '11:40',
            'predmet': 'Čj',
        },
        {
            'hodina': 5,
            'od': '11:50',
            'do': '12:35',
            'predmet': 'In',
        },
        {
            'hodina': 6,
            'od': '12:45',
            'do': '13:30',
            'predmet': 'Nj',
        },
    ],
    3: [
        {
            'hodina': 1,
            'od': '8:00',
            'do': '8:45',
            'predmet': 'Ch',
        },
        {
            'hodina': 2,
            'od': '8:55',
            'do': '9:40',
            'predmet': 'Př',
        },
        {
            'hodina': 3,
            'od': '10:00',
            'do': '10:45',
            'predmet': 'M',
        },
        {
            'hodina': 4,
            'od': '10:55',
            'do': '11:40',
            'predmet': 'Fy',
        },
        {
            'hodina': 5,
            'od': '11:50',
            'do': '12:35',
            'predmet': 'Čj',
        },
        {
            'hodina': 6,
            'od': '12:45',
            'do': '13:30',
            'predmet': 'Ov',
        },
        {
            'hodina': 7,
            'od': '14:00',
            'do': '14:45',
            'predmet': 'Pč',
            'lichy': True,
        },
        {
            'hodina': 7,
            'od': '14:00',
            'do': '14:45',
            'predmet': 'Vv',
            'sudy': True,
        },
        {
            'hodina': 8,
            'od': '14:45',
            'do': '15:30',
            'predmet': 'Pč',
            'lichy': True,
        },
        {
            'hodina': 8,
            'od': '14:45',
            'do': '15:30',
            'predmet': 'Vv',
            'sudy': True,
        },
    ],
    4: [
        {
            'hodina': 1,
            'od': '8:00',
            'do': '8:45',
            'predmet': 'Tv',
        },
        {
            'hodina': 2,
            'od': '8:55',
            'do': '9:40',
            'predmet': 'Tv',
        },
        {
            'hodina': 3,
            'od': '10:00',
            'do': '10:45',
            'predmet': 'Ch',
        },
        {
            'hodina': 4,
            'od': '10:55',
            'do': '11:40',
            'predmet': 'Aj',
        },
        {
            'hodina': 5,
            'od': '11:50',
            'do': '12:35',
            'predmet': 'M',
        },
        {
            'hodina': 6,
            'od': '12:45',
            'do': '13:30',
            'predmet': 'Čj',
        },
        {
            'hodina': 7,
            'od': '14:00',
            'do': '14:45',
            'predmet': 'ZV',
            'lichy': True,
        },
        {
            'hodina': 8,
            'od': '14:45',
            'do': '15:30',
            'predmet': 'ZV',
            'lichy': True,
        },
    ],
    5: [
        {
            'hodina': 1,
            'od': '8:00',
            'do': '8:45',
            'predmet': 'Z',
        },
        {
            'hodina': 2,
            'od': '8:55',
            'do': '9:40',
            'predmet': 'Fy',
        },
        {
            'hodina': 3,
            'od': '10:00',
            'do': '10:45',
            'predmet': 'Nj',
        },
        {
            'hodina': 4,
            'od': '10:55',
            'do': '11:40',
            'predmet': 'D',
        },
        {
            'hodina': 5,
            'od': '11:50',
            'do': '12:35',
            'predmet': 'PZ',
        },
        {
            'hodina': 6,
            'od': '12:45',
            'do': '13:30',
            'predmet': 'PZ',
        },
    ],

}

ICONS = {
    "clearsky_day": "wi-day-sunny.svg",
    "clearsky_night": "wi-night-clear.svg",
    "fair_day": "wi-day-sunny-overcast.svg",
    "fair_night": "wi-night-alt-partly-cloudy.svg",
    "partlycloudy_day": "wi-day-cloudy.svg",
    "partlycloudy_night": "wi-night-alt-cloudy.svg",
    "cloudy": "wi-cloud.svg",
    "rainshowers_day": "wi-day-showers.svg",
    "rainshowers_night": "wi-night-alt-showers.svg",
    "rainshowersandthunder_day": "wi-day-thunderstorm.svg",
    "rainshowersandthunder_night": "wi-night-alt-thunderstorm.svg",
    "sleetshowers_day": "wi-day-sleet.svg",
    "sleetshowers_night": "wi-night-alt-sleet.svg",
    "snowshowers_day": "wi-day-snow.svg",
    "snowshowers_night": "wi-night-alt-snow.svg",
    "rain": "wi-showers.svg",
    "heavyrain": "wi-rain.svg",
    "heavyrainandthunder": "wi-thunderstorm.svg",
    "sleet": "wi-sleet.svg",
    "snow": "wi-snow.svg",
    "snowandthunder": "wi-snow.svg",
    "fog": "wi-fog.svg",
    "sleetshowersandthunder_day": "wi-day-sleet-storm.svg",
    "sleetshowersandthunder_night": "wi-night-alt-sleet-storm.svg",
    "snowshowersandthunder_day": "wi-day-snow-thunderstorm.svg",
    "snowshowersandthunder_night": "wi-night-alt-snow-thunderstorm.svg",
    "rainandthunder": "wi-thunderstorm.svg",
    "sleetandthunder": "wi-storm-showers.svg",
    "lightrainshowersandthunder_day": "wi-day-storm-showers.svg",
    "lightrainshowersandthunder_night": "wi-night-alt-storm-showers.svg",
    "heavyrainshowersandthunder_day": "wi-day-thunderstorm.svg",
    "heavyrainshowersandthunder_night": "wi-night-alt-thunderstorm.svg",
    "lightssleetshowersandthunder_day": "wi-day-sleet-storm.svg",
    "lightssleetshowersandthunder_night": "wi-night-alt-sleet-storm.svg",
    "heavysleetshowersandthunder_day": "wi-day-sleet-storm.svg",
    "heavysleetshowersandthunder_night": "wi-night-alt-sleet-storm.svg",
    "lightssnowshowersandthunder_day": "wi-day-snow-thunderstorm.svg",
    "lightssnowshowersandthunder_night": "wi-night-alt-snow-thunderstorm.svg",
    "heavysnowshowersandthunder_day": "wi-day-snow-thunderstorm.svg",
    "heavysnowshowersandthunder_night": "wi-night-alt-snow-thunderstorm.svg",
    "lightrainandthunder": "wi-storm-showers.svg",
    "lightsleetandthunder": "wi-storm-showers.svg",
    "heavysleetandthunder": "wi-storm-showers.svg",
    "lightsnowandthunder": "wi-storm-showers.svg",
    "heavysnowandthunder": "wi-storm-showers.svg",
    "lightrainshowers_day": "wi-day-showers.svg",
    "lightrainshowers_night": "wi-night-alt-showers.svg",
    "heavyrainshowers_day": "wi-day-rain.svg",
    "heavyrainshowers_night": "wi-night-alt-rain.svg",
    "lightsleetshowers_day": "wi-day-sleet.svg",
    "lightsleetshowers_night": "wi-night-alt-sleet.svg",
    "heavysleetshowers_day": "wi-day-sleet.svg",
    "heavysleetshowers_night": "wi-night-alt-sleet.svg",
    "lightsnowshowers_day": "wi-day-snow.svg",
    "lightsnowshowers_night": "wi-night-alt-snow.svg",
    "heavysnowshowers_day": "wi-day-snow.svg",
    "heavysnowshowers_night": "wi-night-alt-snow.svg",
    "lightrain": "wi-showers.svg",
    "lightsleet": "wi-sleet.svg",
    "heavysleet": "wi-sleet.svg",
    "lightsnow": "wi-snow.svg",
    "heavysnow": "wi-snow.svg",
}


VOLNA = {
    # skola
    date(2023, 10, 26): 'Podzimní prázdniny',
    date(2023, 10, 27): 'Podzimní prázdniny',
    
    date(2023, 12, 25): 'Vánoční prázdniny',
    date(2023, 12, 26): 'Vánoční prázdniny',
    date(2023, 12, 27): 'Vánoční prázdniny',
    date(2023, 12, 28): 'Vánoční prázdniny',
    date(2023, 12, 29): 'Vánoční prázdniny',
    
    date(2024, 1, 1): 'Vánoční prázdniny',
    date(2024, 1, 2): 'Vánoční prázdniny',

    date(2024, 2, 2): 'Pololetní prázdniny',

    date(2024, 2, 19): 'Jarní prázdniny',
    date(2024, 2, 20): 'Jarní prázdniny',
    date(2024, 2, 21): 'Jarní prázdniny',
    date(2024, 2, 22): 'Jarní prázdniny',
    date(2024, 2, 23): 'Jarní prázdniny',

    date(2024, 3, 28): 'Velikonoční prázdniny',

    # svatky
    date(2023, 9, 28): 'Den české státnosti',
    date(2023, 10, 28): 'Den vzniku Československa',
    date(2023, 11, 17): 'Den boje za svobodu a demokracii',
    date(2024, 3, 29): 'Velký pátek',
    date(2024, 4, 1): 'Velikonoční pondělí',
    date(2024, 5, 1): 'Svátek práce',
    date(2024, 5, 8): 'Den vítězství',
    date(2024, 7, 5): 'Den věrozvěstů Cyrila a Metoděje',
    date(2024, 7, 6): 'Den upálení mistra Jana Husa',
}

POVINNOSTI = {
    1: ['Vysávání'],
    4: ['Vysávání', 'Úklid pokoje'],
}

def process_pocasi(now):
    # ziskej data o pocasi
    r = requests.get('http://nuc.lan/pocasi/pocasi-latest.json')
    r.raise_for_status()

    # nalezeni nejblizsi hodiny ktera je nasobkem 6 (diva se do minulosti)
    t = now.floor('hour')
    t = t.replace(hour=t.hour // 6 * 6)

    # vypocat klicovych okamziku
    look_for = [
        t.shift(hours=6),
        t.shift(hours=12),
        t.shift(hours=18),
    ]
    look_for = [i.to('utc').strftime('%Y-%m-%dT%H:%M:%SZ') for i in look_for]

    # iteruj nad jednotlivymi zaznamy a najdi ty co hledame
    first = True
    out = []
    for item in r.json()[0]["properties"]["timeseries"]:
        if first:
            first = False
        elif item['time'] not in look_for:
            continue

        item['data']['next_6_hours']['summary']['icon'] = f"http://nuc.lan/pocasi/svg/{ICONS[item['data']['next_6_hours']['summary']['symbol_code']]}"
        out.append(item)
        if len(out) == 4:
            break

    for item in out:
        hour = arrow.get(item['time']).to('Europe/Prague').hour
        if hour >= 0 and hour < 6:
            item['title'] = 'Ráno'
        elif hour >= 6 and hour < 12:
            item['title'] = 'Dopoledne'
        elif hour >= 12 and hour < 18:
            item['title'] = 'Odpoledne'
        else:
            item['title'] = 'Noc'

    # TODO: preklad symbol_code na nejake jine jmeno souvisejici s ikonou
    # TODO: nadposy pro jednotliva casova obdobi
    # (noc, dopoledne, odpoledne, vecer)
    return out


@app.route("/")
def hello_world():
    # co je za den
    now = arrow.now('Europe/Prague')
    display_tomorrow = now.time().hour >= 19

    # pocasi
    pocasi = process_pocasi(now)

    # volno?
    volno = False
    reason = None
    if (not display_tomorrow and now.isoweekday() in (6, 7)) or (display_tomorrow and now.isoweekday() in (5, 6)):
        volno = True
        reason = 'Víkend!'
    elif (not display_tomorrow and now.date() in VOLNA) or (display_tomorrow and now.shift(days=1).date() in VOLNA):
        volno = True
        reason = VOLNA[now.date()]

    # obedy
    obed = None
    if not volno:
        r = requests.get('http://nuc.lan/obedy/obedy-latest.json')
        r.raise_for_status()
        for item in r.json():
            if item['date'] == now.strftime('%Y-%m-%d'):
                obed = item
                break
        if obed:
            polevka, lunch1 = obed['lunch1'].split('\n')
            obed['lunch1'] = lunch1.strip()
            if obed.get('lunch2'):
                obed['lunch2'] = obed['lunch2'].split('\n')[1].strip()
            obed['polevka'] = polevka.strip()

    # komiks
    fun = None
    if volno:
        feed = feedparser.parse('https://xkcd.com/atom.xml')
        for item in feed.entries:
            soup = BeautifulSoup(item.summary)
            soup.img.attrs['style'] = 'width:100%; height:auto'
            fun = str(soup)

    if display_tomorrow:
        isoweekday = now.shift(days=1).isoweekday()
    else:
        isoweekday = now.isoweekday()
    
    data = {
        'now': now,
        'weekday': WEEKDAYS[now.isoweekday()],
        'month': MONTHS[now.month],
        'rozvrh': ROZVRH.get(isoweekday),
        'krouzky': KROUZKY.get(isoweekday),
        'obed': obed,
        'pocasi': pocasi,
        'volno': volno,
        'reason': reason,
        'povinnosti': POVINNOSTI.get(now.isoweekday(), None),
        'fun': fun,
        'display_tomorrow': display_tomorrow,
    }
    return render_template('index.html', **data)
