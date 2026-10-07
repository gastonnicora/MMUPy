



class PF:
    
    def __init__(self):
        self.page_faults_cant = 0
        self.page_faults=[]
        
    def add_page_fault(self, page_fault: bool):
        if page_fault:
            self.page_faults_cant += 1
        self.page_faults.append(page_fault)