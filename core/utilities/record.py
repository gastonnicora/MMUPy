
from copy import copy, deepcopy

from ..memory.queue import Queue

class Record:
    
    def __init__(self):
        self.queues=[]
        
        self._snapshots = [] 
    
    def add_queue(self, queue:Queue):
        new_queue = copy(queue)
        self.queues.append(new_queue)
        self._snapshots.append(deepcopy(self.queues))
        
    def get_snapshot(self, index: int) -> list:
        return self._snapshots[index]

    def get_record_pages(self, i: int = None):

        pages = []
        index = {}

        queues = (
            self._snapshots[i]
            if i is not None
            else self.queues
        )

        for queue in queues:

            for frame in queue.frames:

                page = frame.page

                if page is None:
                    continue

                if page in index:
                    pages[index[page]] = None

                index[page] = len(pages)
                pages.append(page)

        return [
            page
            for page in pages
            if page is not None
        ]
  
    
    def __repr__(self):
        return "\n".join(
            str(queue)
            for queue in self.queues
        )