import sqlite3

import requests
from fastapi import Request
from ua_parser import user_agent_parser


def create_connection_and_tables(filename):
    try:
        conn = sqlite3.connect(filename)
        return conn
    except Exception as e:
        print(f'Error: {e}')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def is_bot(request: Request):
    user_agent = request.headers.get('user-agent')
    if not user_agent:
        return True

    user_agent = user_agent.lower()
    bot_ua = ['bot', 'lighthouse', 'pingdom', 'crawl', 'spider', 'google', 'curl', 'headlesschrome', 'python', 'axios',
              'wget']
    for ua in bot_ua:
        if ua.lower() in user_agent:
            return True

    return False


def get_geo_location(ip_addr):
    try:
        r = requests.get(f'http://ip-api.com/json/{ip_addr}', timeout=60)
        data = r.json()
        country = data.get('country')
        region = data.get('regionName')
        city = data.get('city')
        return country, region, city
    except:
        return None, None, None


def get_source(referrer):
    return referrer


def get_browser(user_agent):
    parsed_ua = user_agent_parser.Parse(user_agent)
    return parsed_ua.get('user_agent', {}).get('family', '').replace('Mobile', '').strip()


def get_os(user_agent):
    parsed_ua = user_agent_parser.Parse(user_agent)
    os = parsed_ua.get('os', {}).get('family')
    return parsed_ua.get('os', {}).get('family')


def get_device(screen_width, screen_height):
    min_dimension = min(screen_width, screen_height)
    if min_dimension <= 480:
        return 'Mobile'
    elif 480 < min_dimension <= 768:
        return 'Tablet'
    else:
        return 'Desktop'
