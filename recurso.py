import mesa

class Recurso(mesa.Agent):
    def __init__(self,model,reference):
        super().__init__(model)
        self.peso = 0
        self.vu = 0
        self.type = reference
        self.collector = ""

        if self.type == 1:
            self.type = "(C)"
            self.peso = 1
            self.vu = 10
        elif self.type == 2:
            self.type = "(B)"
            self.peso = 1
            self.vu = 20
        else:
            self.type = "(E)"
            self.peso = 2
            self.vu = 50
    
    def step(self):
        pass