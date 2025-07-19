import time

import requests
import schedule
from icecream import ic
from nslookup import Nslookup

from config import (
    API_TOKEN_KENTOES_DOT_COM,
    BASE_API_URL,
    DOMAIN_KENTOES_DOT_COM,
    EMAIL_KENTOES_DOT_COM,
    GET_IP_URL,
    RECORD_ID_KENTOES_DOT_COM,
    ZONE_ID_KENTOES_DOT_COM,
)


def main():
    old_ip = fetch_old_ip()
    current_ip = fetch_current_ip()
    ic(old_ip, current_ip)
    if old_ip != current_ip:
        ic("Update DNS")
        update_dns(current_ip)
    else:
        ic("Nothing Changed")


def fetch_old_ip():
    domain = DOMAIN_KENTOES_DOT_COM
    # dns_query = Nslookup(dns_servers=["1.1.1.1", "8.8.8.8"])
    dns_query = Nslookup()
    ips_record = dns_query.dns_lookup(domain)
    return str(ips_record.answer[0])


def fetch_current_ip():
    req = requests.get(GET_IP_URL)
    result = req.content.decode("utf-8")
    return result


def update_dns(current_ip):
    req = requests.put(
        f"{BASE_API_URL}/{ZONE_ID_KENTOES_DOT_COM}/dns_records/{RECORD_ID_KENTOES_DOT_COM}",
        json={
            "type": "A",
            "name": DOMAIN_KENTOES_DOT_COM,
            "content": current_ip,
            "ttl": 1,
            "proxied": False,
        },
        headers={
            "X-Auth-Email": EMAIL_KENTOES_DOT_COM,
            "X-Auth-Key": API_TOKEN_KENTOES_DOT_COM,
            "Content-Type": "application/json",
        },
    )
    if req.status_code != 200:
        ic(req.text)
    ic(req.json())


if __name__ == "__main__":
    ic("Application started")
    main()
    # excute every 5 minutes
    schedule.every(5).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
