from dataclasses import dataclass
from substrate import Substrate
import pdb

@dataclass
class Interaction:
  substrate1: Substrate
  substrate2: Substrate
  behavior: str
  rate: float = None