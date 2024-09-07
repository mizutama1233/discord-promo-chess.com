import json
import random
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import requests

proxylist = requests.get('https://raw.githubusercontent.com/r00tee/Proxy-List/main/Socks5.txt').text.split()
genduuid = uuid.uuid1()
lock = Lock()
url = "https://www.chess.com/rpc/chesscom.partnership_offer_codes.v1.PartnershipOfferCodesService/RetrieveOfferCode"
tpe = ThreadPoolExecutor(max_workers=25)
session = requests.Session()
webhook = ""
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ja,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "referrer": "https://www.chess.com/play/computer/discord-wumpus?utm_source=chesscom&utm_medium=homepagebanner&utm_campaign=discord2024"
}

def gen(user):
    try:
        data = {
            "userUuid": user["uuid"],
            "campaignId": "4daf403e-66eb-11ef-96ab-ad0a069940ce"
        }

        tp = random.choice(proxylist)
        proxy = {
            "http": "socks5://" + tp,
            "https": "socks5://" + tp,
        }

        response = session.post(
            url,
            headers=headers,
            json=data,
            proxies=proxy,
            verify=False,
            timeout=5
        )
        print(response)
        if response.status_code == 200:
            code_value = response.json().get("codeValue")
            if code_value:
                content_data = {"content": f"<https://discord.com/billing/promotions/{code_value}>"}

                with lock:
                    session.post(webhook, data=json.dumps(content_data), headers={"Content-Type": "application/json"})
                with lock:
                    with open(f"{genduuid}.txt", "a") as f:
                        f.write(f"https://discord.com/billing/promotions/{code_value}\n")
        else:
            print(f"Failed with status code: {response.status_code}")

    except Exception as e:
        print(f"Error occurred: {e}")

while True:
    gamelist = session.get(f'https://www.chess.com/service/gamelist/top?limit=50&from={random.randint(0, 1000)}').json()
    for game in gamelist:
        for user in game["players"]:
            tpe.submit(gen, user)