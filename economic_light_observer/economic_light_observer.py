from economic_light_observer.base import EconomicLightCrawler, EconomicLight

class EconomicLightObserver():
  def __init__(
      self,
      economic_crawler: EconomicLightCrawler
  ) -> None:
     self._economic_crawler = economic_crawler
  
  async def analyze(self) -> str:
    latest_month = await self._economic_crawler.get_latest_month()
    lights = await self._economic_crawler.get_lights()

    observed_months = 3
    last_x_lights = lights[0:observed_months]
    
    ret = ""
    if last_x_lights == [EconomicLight.紅燈]*observed_months:
        ret = f"{latest_month.strftime('%Y/%m')} 景氣過熱 連續{observed_months}個{EconomicLight.紅燈.name}"        
    elif lights == [EconomicLight.藍燈]*observed_months:
        ret = f"{latest_month.strftime('%Y/%m')} 景氣低迷 連續{observed_months}個{EconomicLight.藍燈.name}"
    else:
        ret = f"{latest_month.strftime('%Y/%m')} 景氣正常: {[EconomicLight(month).name for month in last_x_lights]}"        
    
    return ret
