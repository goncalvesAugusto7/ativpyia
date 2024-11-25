import mesa

class Base(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.type = "@"
        self.storage = []

class Obstaculo(mesa.Agent):
    def __init__(self,model,reference):
        super().__init__(model)
        self.type = reference
        if self.type == 1:
            self.type = "*"
        else:
            self.type = "#"

class Recurso(mesa.Agent):
    def __init__(self,model,reference):
        super().__init__(model)
        self.peso = 0
        self.vu = 0
        self.type = reference

        if self.type == 1:
            self.type = "C"
            self.peso = 1
            self.vu = 10
        elif self.type == 2:
            self.type = "B"
            self.peso = 1
            self.vu = 20
        else:
            self.type = "E"
            self.peso = 2
            self.vu = 50

class AgenteSimples(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.inventory = []
        

class Ambiente(mesa.Model):
    def __init__(self, size):
        super().__init__()
        if size < 5:
            size = 5
        self.grid = mesa.space.MultiGrid(size, size, torus=False)

        #Limite de passos
        self.clock_to_storm = size*self.random.randint(1,size)

        # Adicionando Obstaculos
        for _ in range(size+size//3):
            obstaculo_type = self.random.randint(1,2)
            obs = Obstaculo(self,obstaculo_type)
            coords_obs = (self.random.randrange(0,size), self.random.randrange(0,size))
            self.grid.place_agent(obs, coords_obs)
        
        #Adicionando Recursos
        for _ in range(size+self.random.randint(0,size)):
            recurso_type = self.random.randint(1,3)
            rec = Recurso(self,recurso_type)
            coords_rec = (self.random.randrange(0,size), self.random.randrange(0,size))
            self.grid.place_agent(rec, coords_rec)

        #Adicionando a Base
        base = Base(self)
        self.grid.place_agent(base, (size//2,size//2))
    
    def step(self):
        self.display_grid()
        self.clock_to_storm -= 1
        print(f"{self.clock_to_storm} steps to storm")

    def display_grid(self):
        # Cria uma matriz representando o grid
        grid_representation = [["_" for _ in range(self.grid.width)] for _ in range(self.grid.height)]
        for agent in model.agents:
            x = agent.pos[0]
            y = agent.pos[1]
            grid_representation[x][y] = agent.type

        for i in range(len(grid_representation)):
            print(' '.join(map(str, grid_representation[i])))

model = Ambiente(10)
model.step()
            
            

