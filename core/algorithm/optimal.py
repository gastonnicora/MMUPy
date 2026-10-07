from core.algorithm.algorithm import Algorithm
from core.memory.frame import Frame


class Optimal(Algorithm):
    def select_frame(self, index: int) -> Frame:
        farthest = -1
        victim = None

        for f in self.memory.frames:
            if f.page is None:
                continue
            pn = f.page.number

            # Buscar la próxima vez que se usa pn en refs[index+1:]
            next_use = -1
            for i in range(index + 1, len(self.refs)):
                if self.refs[i][0] == pn:
                    next_use = i
                    break

            # Si nunca se usa → candidato ideal (infinito)
            if next_use == -1:
                return f  # reemplazo inmediato, no se va a usar más

            if next_use > farthest:
                farthest = next_use
                victim = f

        if victim is not None:
            return victim

        return self.queue.frames[0]   

    def referenced(self, frame: Frame):
        pass
