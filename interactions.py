from dataclasses import dataclass
from substrate import Enzyme
from substrate import Protein
from substrate import Influence
import pdb

@dataclass
class Interaction:
  substrate1: Substrate
  substrate2: Substrate
  behavior: str
  rate: float = None
