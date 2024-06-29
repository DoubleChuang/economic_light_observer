# -*- coding: utf-8 -*-
import asyncio
from decouple import config
from economic_light_observer.economic_light_observer import EconomicLightObserver
from economic_light_observer.crawler.taiwan import TaiwanEconomicLightCrawler
import requests

import nest_asyncio
nest_asyncio.apply()


LINE_NOTIFY_TOKEN = config('LINE_NOTIFY_TOKEN', cast=str,  default='') 
LINE_NOTIFY_URL = config('LINE_NOTIFY_URL', cast=str,  default="https://notify-api.line.me/api/notify")

tip = """""

－－－－－－－－－－－－－
📝 說明：

連續三個 🔴紅燈: 
    股市過熱
    可能會有大幅回調

連續三個 🔵藍燈: 
    股市低迷
    可以進場買進
    （回測往下最多10%而已）

    -- By 財經Ｍ平方 Ryan
－－－－－－－－－－－－－
"""

def send_line_notify(message, token):
    url = LINE_NOTIFY_URL
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "message": message
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        print(f"Line Notify通知已發送: {message}")
    else:
        print("無法發送Line Notify通知")

async def main():
    taiwan_economic_observer = EconomicLightObserver(TaiwanEconomicLightCrawler("https://index.ndc.gov.tw/n/zh_tw"))
    message = await taiwan_economic_observer.analyze()
    
    send_line_notify(f"\n{message}{tip}", LINE_NOTIFY_TOKEN)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())