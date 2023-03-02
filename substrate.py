from dataclasses import dataclass
import pdb

@dataclass
class Substrate:
  name: str
  substrateType: str
  initialValue: float = 0.0
  phosRate: float = 1.0
  dephosRate: float = -0.1
  maxValue: float = None
  timeStart: int = None
  timeEnd: int = None
  currentValue: float = initialValue