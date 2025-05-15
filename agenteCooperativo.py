import math
from agenteObjetivos import Baseado_Objetivos
from agenteSimples import Reativo_Simples
from base import Base
from recurso import Recurso

class Cooperativo(Baseado_Objetivos):
    def __init__(self, model):
        super().__init__(model)
        self.type = "|coop|"
        self.buddy = None
        self.destiny_estrutura = None

    def step(self):
        print(f"-> AGENTE {self.__class__.__name__} {self.type}_{self.unique_id}__________________________________________________")

        if self.state != "BDI_Ordenado":
            if self.state != "coletando_recurso" and not self.get_estrutura():  

                print(f"\t> {self.__class__.__name__} {self.type}_{self.unique_id} está se comportando como Agente Baseado em Objetivos*")
                # Primeiro, o agente deposita seus itens na base. É necessário estar na vizinhança da base e ter itens no inventário
                if not self.deposite_inventory():
                    # Caso não deposite, o agente verifica se há itens para coletar em sua vizinhança
                    if self.resources_in_neighborhood() != True:
                        # Se não houver ele se move para outra célula
                        if not self.go_to_nearest_resource():
                            self.move()
                    else:
                        # Se houver, ele coleta um item
                        self.collect_resources()
                        self.state = "retornando_base"
                        print(f"\t> {self.type}_{self.unique_id} esta em {self.pos}\n")

                self.regist()
                
                #print(f"\t> celulas exploradas: {self.model.explored_cells}")
                
            # Impressao do estado e do inventario do agente
            print(f"\t> Estado de {self.type}_{self.unique_id}: {self.state}")
            self.print_inventory()
            print()
        

    def get_estrutura(self):
        # Verificando se já há uma estrutura escolhida
        if self.destiny_estrutura is None:
            return self.select_estrutura()
        else:
            if self.buddy:
                print(f"Buddy: {self.buddy.type}_{self.buddy.unique_id}")

            if not self.go_to_estrutura():
                if not self.collect_estrutura():
                    if not self.get_buddy():
                        if not self.call_buddy():
                            if not self.return_base_with_estrutura():
                                if not self.deposite_estrutura():
                                    return False
        return True

    '''Função para escolher a estrutura'''
    def select_estrutura(self):
        if self.model.found_estruturas:  # Verificando se há uma estrutura antiga descoberta 
            # Pegando a estrutura mais próxima
            self.destiny_estrutura = min(self.model.found_estruturas, key=lambda coord: math.dist(coord, self.pos))
            return True
        
        return False

    '''Função para ir até a estrutura encontrada mais próxima'''  # Pré-requisitos: o estado não ser 'atras_recurso' ou 'retornando_base'
    def go_to_estrutura(self):
        if not self.inventory:
            estrutura = self.model.grid.get_cell_list_contents([self.destiny_estrutura])[0]
            print(estrutura.pos)

            if not estrutura in self.neighbors() and not self.inventory:
                self.state = "atras_estrutura"  # Estado do agente

                # Define o próximo passo em direção ao destino
                destiny_step_estrutura = min(self.get_possible_steps(), key=lambda coord: math.dist(coord, self.destiny_estrutura))

                # Move o agente para o próximo passo em direção ao destino
                self.model.grid.move_agent(self, destiny_step_estrutura)
                return True

            print(f"\t\t> Estado de {self.type}_{self.unique_id}: {self.state}")
        return False

    '''Função para coletar a estrutura''' 
    def collect_estrutura(self):
        if self.state not in ["atras_recurso", "retornando_base", "coletando_estrutura", "retornando_base_com_buddy"]:
            estrutura = self.model.grid.get_cell_list_contents([self.destiny_estrutura])[0]
            print(estrutura)
                
            # Colocando estrutura no inventário
            self.inventory.append(estrutura)
            self.state = "coletando_estrutura"

            # Remover o item do dicionário found_resources
            if estrutura.pos in self.model.found_resources:
                del self.model.found_resources[estrutura.pos]
                self.model.found_estruturas.remove(estrutura.pos)

            # Atualizando informações
            self.collected_vu += 50

            # Move o agente para a posição do item
            self.model.grid.move_agent(self, estrutura.pos)

            # Setando o tipo da estrutura
            estrutura.type = "Estrutura Antiga"

            # Removendo da grid
            self.model.grid.remove_agent(estrutura)
            self.model.schedule.remove(estrutura)

            return True

        return False

    '''Função para encontrar um buddy'''
    def get_buddy(self):
        if not self.buddy:
            # Listando os agentes colegas
            colegas = [] 
            for agente in self.model.schedule.agents:
                if isinstance(agente, Reativo_Simples) and agente != self and agente.type != "[[@]]":
                    colegas.append(agente)

            # Listando os agentes colegas que podem ajudar
            possible_buddys = []  # Guarda as coordenadas dos buddys que podem ajudar
            for colega in colegas:
                if colega.state != "retornando_base" and colega.state != "coletando_recurso" and colega.state != "atras_recurso":
                    possible_buddys.append(colega.pos)
            
            if possible_buddys:
                coords_buddy = min(possible_buddys, key=lambda coord: math.dist(coord,self.pos)) 
                self.buddy = self.model.grid.get_cell_list_contents([coords_buddy])[0]
                if hasattr(self.buddy, "state"):
                    self.buddy.state = "cooperando"
            return True
        
        return False

    '''Função para chamar um buddy para ajudar'''
    def call_buddy(self):
        if self.inventory:
            # Se o buddy estiver do lado do agente coop, ele ocupará a mesma célula
            print(f"Buddy: {self.buddy}")
            if self.buddy in self.neighbors():
                self.model.grid.move_agent(self.buddy, self.pos)
                self.type = "|co/" + self.buddy.type[1] + self.buddy.type[2] + "|"
                return True

            # Se o buddy ainda não tiver alcançado o agente coop
            if self.buddy.pos != self.pos:
                next_buddy_step = min(self.buddy.get_possible_steps(), key=lambda coord: math.dist(coord, self.pos))
                self.model.grid.move_agent(self.buddy, next_buddy_step)
                return True

        return False

    '''Função de retorno à base'''
    def return_base_with_estrutura(self):
        # Se ainda não estiverem na vizinhança da estrutura
        neighborhood = self.model.grid.get_neighborhood(
            self.coords_base,
            moore=True,
            include_center=False
        )
        if not self.pos in neighborhood:
            self.state = "retornando_base_com_buddy"
            possible_steps = self.get_possible_steps()
            if possible_steps:
                next_coord = min(possible_steps, key=lambda coord: math.dist(coord, self.coords_base))
                self.model.grid.move_agent(self, next_coord)
                if self.buddy:
                    self.model.grid.move_agent(self.buddy, next_coord)

                return True

        return False

    '''Função para depositar na base'''
    def deposite_estrutura(self): 
        #verificando se o agente coop esta na vizinhanca da base 
        neighborhood = self.model.grid.get_neighborhood( self.coords_base, moore = True, include_center = False ) 
        if self.pos in neighborhood: 
            base = self.model.grid.get_cell_list_contents([self.coords_base])[0] 
            estrutura = self.inventory[0] 

            #incrementando o vu do buddy 
            self.buddy.collected_vu += 50 

            #depositando 
            base.storage.append(estrutura) 
            estrutura.collector = f"|coop|_{self.unique_id} e {self.buddy.type}_{self.buddy.unique_id}" 
            print(f"\t >Estrutura Antiga depositado por {estrutura.collector}") 

            #reiniciando os atributos 
            self.type = "|coop|" 
            self.inventory.clear() 
            self.state = "" 
            if hasattr(self.buddy, "state"): 
                self.buddy.state = "" 
            self.buddy = None 
            self.destiny_estrutura = None 

            return True 
        
        return False