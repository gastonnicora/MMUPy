"""Estado de la simulación correspondiente a un paso."""

from dataclasses import dataclass


@dataclass
class StepState:
    """Representa el estado completo generado por una referencia."""

    ref: str
    page_number: str
    is_modified: bool
    is_page_fault: bool
    page_faults_total: int
    state_msg: str
    frames: list
