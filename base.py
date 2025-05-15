import mesa

class Base(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.type = "[[@]]"
        self.storage = []
    
    def step(self):
        pass