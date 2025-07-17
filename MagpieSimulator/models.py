from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class SegmentState:
    id: int
    col: List[List[int]]  # List of RGB color lists


@dataclass
class WLEDState:
    on: bool
    bri: int
    name: str
    seg: List[SegmentState]
    fx: Optional[int] = None  # Effect ID, e.g., 68 for Pride


class State:
    def __init__(
        self, on: bool, seg: Optional[List[Any]] = None, fx: Optional[int] = None
    ) -> None:
        self.on = on
        self.seg = seg
        self.fx = fx
