import mesa

class Obstaculo(mesa.Agent):
    def __init__(self,model,reference):
        super().__init__(model)
        self.type = reference
        if self.type == 1:
            self.type = "{*}"
        else:
            self.type = "{#}"
    
    def step(self):
        pass