"""Motor principal de la simulación de memoria."""

from core.algorithm.fifo import FIFO
from core.algorithm.fifo2 import Fifo2
from core.algorithm.lru import Lru
from core.algorithm.optimal import Optimal
from core.memory.memory import Memory
from core.memory.page import Page
from core.memory.queue import Queue
from core.utilities.pf import PF
from core.utilities.record import Record
from core.utilities.step_state import StepState


def parse_references(text: str) -> list[tuple[str, bool]]:
    """Convierte la cadena de referencias en pares de página y modificación."""
    refs = []
    for token in text.split():
        if token.upper().endswith("M"):
            refs.append((token[:-1], True))
        else:
            refs.append((token, False))
    return refs


class Simulator:
    """Ejecuta la simulación y conserva el estado de cada paso."""

    ALGORITHMS = {
        "FIFO": FIFO,
        "FIFO2": Fifo2,
        "LRU": Lru,
        "OPTIMO": Optimal,
    }

    def __init__(
        self,
        memory_size: int,
        references: str,
        algorithm: str = "FIFO",
    ):
        """Inicializa el simulador y calcula todos los pasos."""
        self.memory_size = memory_size
        self.references_text = references
        self.algorithm_name = algorithm
        self.steps: list[StepState] = []
        self._precompute()

    def _precompute(self):
        """Prepara memoria, algoritmo, contadores y registro histórico."""
        refs = parse_references(self.references_text)
        self.reserved_frames = any(is_modified for _, is_modified in refs)
        self.memory = Memory(
            frame_count=self.memory_size,
            reserved=self.reserved_frames,
        )
        self.queue = Queue()
        algorithm_class = self.ALGORITHMS[self.algorithm_name]
        self.algorithm = algorithm_class(
            queue=self.queue,
            memory=self.memory,
            refs=refs,
        )
        self.pf = PF()
        self.record = Record()

        for step, (page_number, is_modified) in enumerate(refs):
            self.access(page_number, is_modified, step)

    def access(self, page_number: str, is_modified: bool, step: int):
        """Procesa una referencia y guarda el estado resultante."""
        frame = self.memory.find_page(page_number)

        if frame is not None:
            self.algorithm.referenced(frame)
            is_fault = False
            state_msg = "Hit + Modificada" if is_modified else "Hit"
        else:
            frame = Page(page_number)
            frame.valid = True
            memory_frame = self.memory.first_empty()

            if memory_frame is None:
                memory_frame = self.algorithm.select_frame(step)
                memory_frame.page.valid = False

                if self.reserved_frames and memory_frame.page.modified:
                    reserved_frame = self.memory.get_reserved_frame()
                    memory_frame.reserved = True
                    memory_frame.clear()
                    memory_frame = reserved_frame
                    memory_frame.reserved = False

                self.queue.pop()

            memory_frame.load(frame)
            self.queue.push(memory_frame)
            frame = memory_frame
            is_fault = True
            state_msg = "Page Fault" + (" + Modificada" if is_modified else "")

        if is_modified:
            frame.page.modified = True

        self.pf.add_page_fault(is_fault)
        self.record.add_queue(self.queue)

        frames_state = [
            (
                current_frame.page.number,
                current_frame.page.valid,
                current_frame.page.referenced,
                current_frame.page.modified,
                current_frame.reserved,
            )
            if current_frame.page is not None
            else (
                None,
                False,
                False,
                False,
                current_frame.reserved,
            )
            for current_frame in self.memory.frames
        ]

        ref_display = page_number + ("M" if is_modified else "")
        self.steps.append(
            StepState(
                ref=ref_display,
                page_number=page_number,
                is_modified=is_modified,
                is_page_fault=is_fault,
                page_faults_total=self.pf.page_faults_cant,
                state_msg=state_msg,
                frames=frames_state,
            )
        )

    @property
    def total_steps(self) -> int:
        """Devuelve la cantidad de referencias procesadas."""
        return len(self.steps)

    def state_at(self, i: int) -> StepState:
        """Devuelve el estado correspondiente al paso indicado."""
        return self.steps[i]
