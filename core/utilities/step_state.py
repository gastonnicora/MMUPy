
from dataclasses import dataclass

@dataclass
class StepState:
    ref: str
    page_number: str
    is_modified: bool
    is_page_fault: bool
    page_faults_total: int
    state_msg: str
    frames: list  # list of (page_number|None, valid, referenced, modified)   