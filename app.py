import os
import re
from urllib.parse import urlparse, urljoin

import uvicorn
import validators
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from utils import get_source, get_geo_location, get_os, get_device, get_browser, create_connection_and_tables, \
    dict_factory, is_bot

load_dotenv()

db_file = os.getenv('DB_FILE', 'analytics.db')

app = FastAPI()

origins = [
    '*',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='static'), name='static')


class Client(BaseModel):
    client_id: str
    domain: str


class Pageview(BaseModel):
    client_id: str
    user_agent: str
    url: str
    referrer: str
    screen_width: int
    screen_height: int


@app.get('/')
async def index(request: Request):
    conn = create_connection_and_tables(db_file)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients')
    records = []
    for row in cursor.fetchall():
        row['url'] = urljoin(os.getenv('BASE_URL', 'http://127.0.0.1:5000/'), f'/client/{row["client_id"]}')
        records.append(row)

    if len(records) == 0:
        return {'hello': 'world'}
    else:
        return records


@app.get('/client/{client_id}')
async def client(client_id: str):
    conn = create_connection_and_tables(db_file)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pageview WHERE client_id=?', (client_id,))
    records = cursor.fetchall()
    return records


@app.post('/add')
async def add(client: Client):
    domain = client.domain.strip('/')

    valid = validators.domain(domain)
    if not valid:
        if not re.match('127\.0\.0\.1\:\d+', domain) and not re.match('localhost:\d+', domain):
            return {
                'success': False,
                'msg': f'Invalid domain {domain}'
            }

    conn = create_connection_and_tables(db_file)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (client_id, domain) VALUES (?, ?)', (client.client_id, domain))
    conn.commit()
    conn.close()

    return {
        'success': True,
        'msg': f'Added client {client.client_id} - {domain}'
    }


@app.post('/track')
async def track(page_view: Pageview, request: Request):
    if is_bot(request):
        return {
            'success': False,
            'msg': 'bot request'
        }

    conn = create_connection_and_tables(db_file)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    domain = urlparse(page_view.url).netloc
    if domain.startswith('www.'):
        domain = domain.replace('www.', '', 1)

    cursor.execute('SELECT * FROM clients WHERE client_id=?', (page_view.client_id,))
    row = cursor.fetchone()
    if not row:
        return {
            'success': False,
            'msg': 'no client found for the given code'
        }

    if domain.lower() != row['domain'].lower():
        return {
            'success': False,
            'msg': 'client do not match with domain name'
        }

    print(request.headers, flush=True)
    try:
        ip_addr = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    except:
        try:
            ip_addr = request.client.host
        except:
            ip_addr = None

    print(ip_addr, flush=True)
    source = get_source(page_view.referrer)
    country, region, city = get_geo_location(ip_addr)
    browser = get_browser(page_view.user_agent)
    os = get_os(page_view.user_agent)
    device = get_device(page_view.screen_width, page_view.screen_height)
    insert = (page_view.client_id, page_view.url, page_view.referrer, source, ip_addr, country, region, city,
              page_view.user_agent, browser, os, device)
    cursor.execute('''INSERT INTO pageview (client_id, url, referrer, source, ip_addr, country, region, city, 
                        user_agent, browser, os, device) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', insert)
    conn.commit()
    conn.close()
    return {
        'success': True,
        'msg': 'page view tracked'
    }


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 5000)))
