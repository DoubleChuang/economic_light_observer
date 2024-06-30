
from playwright.async_api import async_playwright
from datetime import datetime
from pathlib import PurePath
from economic_light_observer.base import EconomicLight
from decouple import config

class TaiwanEconomicLightPlaywrightCrawler():
  def __init__(self, url: str) -> None:
     super().__init__()
     self._url = url
     self._has_cache = False
     self._months = list()
     self._economic_lights = list()

  async def get_raw_data(self, no_cache: bool=False) -> bool:
    if not no_cache and self._has_cache:
      return self._has_cache
    
    CHROMIUM_EXEC_PATH = config('CHROMIUM_EXEC_PATH', cast=str,  default='/usr/bin/chromium')
    launch_options = {}
    if CHROMIUM_EXEC_PATH != '':
        launch_options['executable_path'] = CHROMIUM_EXEC_PATH
    
    async with async_playwright() as playwright:
      browser = await playwright.chromium.launch(
          **launch_options,
          # headless=False,          
      )
      
      context = await browser.new_context()
      page = await context.new_page()
      
      await page.goto(self._url)      
      await page.wait_for_load_state('networkidle')
      
      months = await page.locator('.highcharts-axis-labels.highcharts-xaxis-labels text').all_text_contents()      
      self._months = [datetime.strptime(month, '%Y/%m') for month in months]
            
      imgs = page.locator('.highcharts-markers.highcharts-tracker image')      
      img_count = await imgs.count()
      self._economic_lights = [
        EconomicLight(PurePath(await imgs.nth(i).get_attribute('href')).stem) for i in range(img_count)
      ]
      
      await context.close()
      await browser.close()
      
    self._has_cache = True
    return self._has_cache

  async def get_months(self)-> list[datetime]:
    await self.get_raw_data()    
    return self._months

  async def get_latest_month(self) -> datetime:
    months = await self.get_months()
    return months[-1]
  
  async def get_lights(self) -> list[EconomicLight]:
    await self.get_raw_data()    
    return self._economic_lights
