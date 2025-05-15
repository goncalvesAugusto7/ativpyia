import mesa
from agenteBDI import BDI
from agenteCooperativo import Cooperativo
from agenteObjetivos import Baseado_Objetivos
from obstaculo import Obstaculo
from recurso import Recurso
from base import Base
from agenteSimples import Reativo_Simples
from agenteEstados import Baseado_Estados

class Ambiente(mesa.Model):
    def __init__(self, size):
        super().__init__()
        if size < 5: size = 5
        self.grid = mesa.space.MultiGrid(size, size, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.explored_cells = []
        self.found_resources = {}
        self.found_estruturas = []
        
        #Limite de passos
        self.clock_to_storm = (size*3)+self.random.randint(size,size*2)

        # Adicionando Obstaculos
        for _ in range(size+size//3):
            obstaculo_type = self.random.randint(1,2)
            obs = Obstaculo(self,obstaculo_type)
            coords_obs = (self.random.randrange(0,size), self.random.randrange(0,size))
            self.grid.place_agent(obs, coords_obs)
            self.schedule.add(obs)
        
        # verifica se uma celula esta vazia
        def clean_cell_if_is_not_empty(pos):

            cell_contents = self.grid.get_cell_list_contents([pos])
            if cell_contents:
                #se houver agentes na celula, remove todos
                for agent in cell_contents:
                    self.grid.remove_agent(agent)
                    self.schedule.remove(agent)
                return True # agentes foram removidos
            return False    #nao haviam agentes
        
        #Adicionando Recursos
        for _ in range(size+self.random.randint(size,size*2)):
            recurso_type = self.random.randint(1,3)
            rec = Recurso(self,recurso_type)
            coords_rec = (self.random.randrange(0,size), self.random.randrange(0,size))
            
            clean_cell_if_is_not_empty(coords_rec)

            self.grid.place_agent(rec, coords_rec)
            self.schedule.add(rec)
        
        #Adicionando a Base
        base = Base(self)
        coords_base = (size//2,size//2)
            #verificando se a celular aleatoria ja estava ocupada
        clean_cell_if_is_not_empty(coords_base)
        
        self.grid.place_agent(base, coords_base)
        self.schedule.add(base)

        #Adicionando Agentes

            #Agente Reativo simples
        ars = Reativo_Simples(self)
        coords_ars = (size//2-1,size//2)

        clean_cell_if_is_not_empty(coords_ars)

        self.grid.place_agent(ars,coords_ars)
        self.schedule.add(ars)

            #Agente Baseado em Estados
        abe = Baseado_Estados(self)
        coords_abe = (size//2,size//2-1)

        clean_cell_if_is_not_empty(coords_abe)

        self.grid.place_agent(abe,coords_abe)
        self.schedule.add(abe)

            #Agente Baseado em Objetivos
        abo = Baseado_Objetivos(self)
        coords_abo = (size//2+1,size//2)

        clean_cell_if_is_not_empty(coords_abo)

        self.grid.place_agent(abo,coords_abo)
        self.schedule.add(abo)

            #Agente Cooperativo
        aco = Cooperativo(self)
        coords_aco = (size//2,size//2+1)

        clean_cell_if_is_not_empty(coords_aco)

        self.grid.place_agent(aco,coords_aco)
        self.schedule.add(aco)

            #Agente BDI
        bdi = BDI(self)
        coords_bdi = (coords_base)

        self.grid.place_agent(bdi,coords_base)
        self.schedule.add(bdi)

    '''---Funcao para imprimir os itens no deposito da base---'''
    def print_storage(self):
        cont = 0
        storage = []

        # Itera sobre os agentes no agendador
        for element in self.schedule.agents:
            if isinstance(element, Base):
                storage = element.storage

        # Imprime o conteúdo do depósito da base
        print("Depósito da Base:")
        if len(storage) > 0:
            for item in storage:
                cont += 1
                print(f"\t> Item {cont}: {item.type}\t{item.collector}")

            for agent in self.grid.agents:
                if isinstance(agent, Reativo_Simples) and agent.type != "[[@]]":
                    print(f"\n\t{agent.collected_vu} valores de unidade coletados por {agent.type}_{agent.unique_id}")
        else:
            print("\t*vazio*")

    def step(self):
        
        print("___")
        self.clock_to_storm -= 1
        print(f"|[{self.clock_to_storm} steps to storm]")
        self.print_storage()
        print("___\n")


        self.agents.shuffle_do("step")

        for agent in self.agents:
            if isinstance(agent, Reativo_Simples) and agent.type != "[[@]]":
                print(f"*Estado de {agent.type}_{agent.unique_id}: {agent.state}")
        print(f"> Lista recursos achados: {self.found_resources}")
        print(f"> Lista estruturas antigas: {self.found_estruturas}\n")

        self.display_grid()

    def display_grid(self):
        # Cria uma matriz representando o 
        print(type(self.found_resources))
        grid_representation = [["_" for _ in range(self.grid.width)] for _ in range(self.grid.height)]     
        for agent in self.schedule.agents:
            x,y = agent.pos
            grid_representation[x][y] = agent.type
        print("\nGrid:") 
        for row in grid_representation: 
            print("\t".join(row))