from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SegmentState:
    id: int
    col: List[List[int]]  # List of RGB color lists


@dataclass
class WLEDState:
    on: bool
    bri: int
    name: str
    seg: List[SegmentState] = field(default_factory=list)
    fx: Optional[int] = None  # Effect ID, e.g., 68 for Pride
