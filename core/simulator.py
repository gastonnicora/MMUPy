from os import remove

from core.algorithm.optimal import Optimal
from core.memory.memory import Memory
from core.utilities.record import Record
from core.memory.queue import Queue
from core.utilities.pf import PF
from core.algorithm.fifo import FIFO
from core.algorithm.fifo2 import Fifo2
from core.algorithm.lru import Lru
from core.memory.page import Page
from core.utilities.step_state import StepState


def parse_references(text: str) -> list[tuple[str, bool]]:
    refs = []
    for token in text.split():
        if token.upper().endswith('M'):
            refs.append((token[:-1], True))
        else:
            refs.append((token, False))
    return refs

class Simulator:
    ALGORITHMS = {
        "FIFO": FIFO,
        "FIFO2": Fifo2,
        "LRU": Lru,
        "OPTIMO":Optimal,
    }

    
    def __init__( self,
        memory_size: int,
        references: str,
        algorithm: str = "FIFO"
    ):
        self.memory_size = memory_size
        self.references_text = references
        self.algorithm_name = algorithm

        self.steps: list[StepState] = []

        self._precompute()
            
    def _precompute(self):
        refs = parse_references(self.references_text)
        self.reserved_frames =  True in [is_modified for _, is_modified in refs]
        self.memory = Memory(frame_count=self.memory_size, reserved=self.reserved_frames)
        self.queue = Queue()
        algorithm_class = self.ALGORITHMS[self.algorithm_name]

        self.algorithm = algorithm_class(
            queue=self.queue,
            memory=self.memory,
            refs=refs
        )

        self.pf = PF()
        self.record = Record()
        step=0
        for page_number, is_modified in refs:
            self.access(page_number, is_modified, step)
            step+=1
    
    def access(self, page_number: str, is_modified: bool,step: int):
        frame = self.memory.find_page(page_number)
        is_fault=""
        if frame is not None:
            self.algorithm.referenced(frame)
            is_fault = False
            if is_modified:
                state_msg = "Hit + Modificada"
            else:
                state_msg = "Hit"
        
        else:
            
            page = Page(page_number)

            page.valid = True

            # Buscar frame vacío
            frame = self.memory.first_empty()

            # Si no hay espacio,
            # FIFO selecciona uno
            if frame is None:
                frame = (
                    self.algorithm.select_frame(step)
                    
                )
                frame.page.valid = False
                if self.reserved_frames and frame.page.modified:
                    frame2=self.memory.get_reserved_frame()
                    frame.reserved = True
                    frame.clear()
                    frame=frame2
                    frame.reserved = False
                self.queue.pop()
                
            frame.load(page)
            
            self.queue.push(frame)
            is_fault = True
            
            state_msg = "Page Fault" + (" + Modificada" if is_modified else "")
        
        if is_modified:
            frame.page.modified = True
        
        self.pf.add_page_fault(is_fault)
        
        self.record.add_queue(self.queue)
        
        frames_state = []
        for f in self.memory.frames:
            if f.page is not None:
                frames_state.append((f.page.number, f.page.valid, f.page.referenced, f.page.modified, f.reserved))
            else:
                frames_state.append((None, False, False, False, f.reserved))

        ref_display = page_number + ("M" if is_modified else "")
        self.steps.append(StepState(
            ref=ref_display,
            page_number=page_number,
            is_modified=is_modified,
            is_page_fault=is_fault,
            page_faults_total=self.pf.page_faults_cant,
            state_msg=state_msg,
            frames=frames_state,
        ))
        
            
    @property
    def total_steps(self) -> int:
        return len(self.steps)

    def state_at(self, i: int) -> StepState:
        print(f"State at step {i}:")
        for r in self.record.get_record_pages(i):
                    print(r)
        print("________________________________________")
        return self.steps[i]   
