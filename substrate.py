from dataclasses import dataclass
import pdb


@dataclass
class Protein:
  name: str
  substrateType: str = 'protein'
  initialValue: float = 0.0
  transRate: float = 1.0
  degradRate: float = -0.1
  currentValue: float = initialValue


@dataclass
class Enzyme:
  name: str
  substrateType: str = 'enzyme'
  initialValue: float = 0.0
  phosRate: float = 1.0
  dephosRate: float = -0.1
  currentValue: float = initialValue


@dataclass
class Influence:
  name: str
  substrateType: str = 'stimulus'
  initialValue: float = 0.0
  maxValue: float = None
  timeStart: int = None
  timeEnd: int = None
  currentValue: float = initialValue