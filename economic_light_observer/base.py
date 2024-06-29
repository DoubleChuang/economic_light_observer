# -*- coding: utf-8 -*-
from enum import Enum
from datetime import datetime
from typing import Protocol

class EconomicLight(str, Enum):
    紅燈 = "light_1"
    橘燈 = "light_2"
    黃燈 = "light_3"
    綠燈 = "light_4"
    藍燈 = "light_5"
    
class EconomicLightCrawler(Protocol):
  def get_latest_month() -> datetime:
    ...
  
  def get_lights() -> list[EconomicLight]:
    ...
