import math
import mesa
import random
from base import Base
from recurso import Recurso

class Reativo_Simples(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.inventory = [] # limite adotado = 1 item
        self.collected_vu = 0
        self.type = "|reat|"
        self.coords_base = self.set_base_coords()
        self.state = ""

    '''---Funcao de acao---'''
    def step(self):
        print(f"-> AGENTE {self.__class__.__name__} {self.type}_{self.unique_id}__________________________________________________")

        if self.state != "cooperando" and self.state != "BDI_Ordenado":

            #primeiro, o agente deposita seus itens na base. E necessario estar na vizinhanca da base e ter itens no inventario
            if not self.deposite_inventory():
                #caso nao deposite, o agente verifica se ha itens para coletar em sua vizinhanca
                if self.resources_in_neighborhood() != True:
                    #se nao houver ele se move para outra celula
                    self.move()
                else: 
                    #se houver, ele coleta um item
                    self.collect_resources()
                    print(f"\t> {self.type}_{self.unique_id} esta em {self.pos}\n")

                #impressao do inventario do agente
            self.print_inventory()
            print()
        

    '''---Funcao para pegar os vizinhos do agente (usa vizinhanca de moore)---'''
    def neighbors(self):
        neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore = True,
            include_center = False
        )
        neighbors = self.model.grid.get_cell_list_contents(neighborhood)
        
        return neighbors
    
    '''---Funcao para receber os possiveis caminhos que o agente pode seguir---'''
    def get_possible_steps(self):
        possible_steps = []
        neighborhood = self.model.grid.get_neighborhood( 
            self.pos, 
            moore=True, 
            include_center=False 
        )

        for cell in neighborhood:
            cell_contents = self.model.grid.get_cell_list_contents([cell])
            if len(cell_contents) == 0:
                possible_steps.append(cell)

        return possible_steps
    
    '''Funcao para coletar os recursos na vizinhanca'''
    def collect_resources(self):
        neighboord = self.neighbors()
        remove_itens = []
        if len(self.inventory) < 1:  # Inventário tem espaço livre
            for item in neighboord:
                if isinstance(item, Recurso):
                    if item.peso == 1:
                        self.inventory.append(item)

                        # Remover o item do dicionário found_resources
                        if item.pos in self.model.found_resources:
                            del self.model.found_resources[item.pos]

                        # Verificar e atualizar destiny dos agentes caso o item que ele estava indo atras ja tenha sido pegado
                        for agent in self.model.grid.agents:
                            if hasattr(agent, "destiny") and agent.destiny == item.pos:
                                agent.destiny = None


                        item.collector = f"{self.type}_{self.unique_id}"
                        self.collected_vu += item.vu
                        remove_itens.append(item)
                        if hasattr(self, "state"):
                            self.state = "coletando_recurso"

                        # Move o agente para a posição do item
                        self.model.grid.move_agent(self, item.pos)

                        # Imprimindo item coletado
                        if item.type == "(C)":
                            item.type = "Cristal Energetico"
                        else:
                            item.type = "Bloco de Metal Raro"

                        print(f"\t> {self.type}_{self.unique_id} coletou {item.type}")
                        break
        else:
            self.move()
            return
        #removendo os itens coletados da grid
        for item in remove_itens:
            self.model.grid.remove_agent(item)
            self.model.schedule.remove(item)
    
    '''Funcao para imprimir o inventario'''
    def print_inventory(self):
        cont = 0
        print(f"\t> Inventario do {self.type}_{self.unique_id}:")
        if len(self.inventory) > 0:
            for item in self.inventory:
                cont += 1
                print(f"\t\t> Item {cont}: {item.type}")
        else:
            print("\t\t*vazio*")


    '''---Função para verificar se há recursos na vizinhança---'''
    def resources_in_neighborhood(self):
        neighbors = self.neighbors()
        for neighbor in neighbors:
            if isinstance(neighbor, Recurso):
                if neighbor.peso == 1:
                    return True
        print(f"\t> Nao ha recursos coletaveis na vizinhanca do {self.type}_{self.unique_id}")
        return False

    '''Função para achar as coordenadas da base'''
    def set_base_coords(self):
        for agent in self.model.schedule.agents:
            if isinstance(agent, Base):
                return agent.pos
        return None

    '''Função para encontrar o caminho de volta à base'''
    def return_base(self):
        base_neighborhood = self.model.grid.get_neighborhood(
            self.coords_base,
            moore=True,
            include_center=False
        )

        # Se o agente não estiver na vizinhança da base
        if not self.pos in base_neighborhood:
            #mudando o estado do agente, caso tenha
            if hasattr(self, "state"):
                self.state = "retornando_base"
            possible_steps = self.get_possible_steps() 
            if possible_steps: 
                next_coord = min(possible_steps, key=lambda coord: math.dist(coord, self.coords_base)) 
                self.model.grid.move_agent(self, next_coord) 
                return True

        return False

    '''---Função para depositar recursos na base---'''
    def deposite_inventory(self):
        depositated_itens = []

        if self.inventory:
            neighbors = self.neighbors()
            for neighbor in neighbors:
                if isinstance(neighbor, Base):
                    for item in self.inventory:
                        neighbor.storage.append(item)
                        depositated_itens.append(item)
                        print(f"\t >{item.type} depositado por {self.type}_{self.unique_id}")
                    self.inventory.clear()
                    return True

            # Se não está na vizinhança da base, retorna à base
            self.return_base()
            return True

        return False
    
    '''Funcao para registrar dados'''
    def regist(self):
    # Registrando células exploradas usando um conjunto para eficiência
        if self.pos not in self.model.explored_cells:  # Evitando repetição de células
            self.model.explored_cells.append(self.pos)

        # Registrando itens encontrados, seus valores de unidade e localizações usando um dicionário
        for item in self.neighbors():
            if isinstance(item, Recurso):
                if item.pos not in self.model.found_resources:
                    self.model.found_resources[item.pos] = item.vu
                    if item.peso == 2:
                        self.model.found_estruturas.append(item.pos)



    '''---Funcao para mover o agente no grid---'''
    def move(self):
        if self.get_possible_steps():
            new_position = random.choice(self.get_possible_steps())
            self.model.grid.move_agent(self,new_position)
            print(f"\t1> {self.type}_{self.unique_id} moveu-se para {new_position}")
            self.model.explored_cells.append(self.pos)