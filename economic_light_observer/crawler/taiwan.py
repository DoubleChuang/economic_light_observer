
from requests_html import requests, AsyncHTMLSession
from datetime import datetime
from pathlib import PurePath
from economic_light_observer.base import EconomicLight

class TaiwanEconomicLightCrawler():
  def __init__(self, url: str) -> None:
     super().__init__()
     self._url = url
     self._response = None

  async def get_raw_data(self, no_cache: bool=False) -> requests.Response:
    if not no_cache and self._response is not None:
      return self._response
    
    session = AsyncHTMLSession()
    self._response = await session.get(self._url)
    await self._response.html.arender(timeout=20, sleep=1, keep_page=True, scrolldown=1)
    return self._response

  async def get_months(self)-> list[datetime]:
    await self.get_raw_data()
    months = self._response.html.find('g.highcharts-axis-labels.highcharts-xaxis-labels text')
    return [datetime.strptime(month.text, '%Y/%m') for month in months]

  async def get_latest_month(self) -> datetime:
    months = await self.get_months()
    return months[-1]
  
  async def get_lights(self) -> list[EconomicLight]:
    await self.get_raw_data()
    lights = self._response.html.find('g.highcharts-markers image')
    return [EconomicLight(PurePath(img.attrs.get('xlink:href')).stem) for img in lights]
