import math
from recurso import Recurso
from agenteSimples import Reativo_Simples

class Baseado_Estados(Reativo_Simples):
    def __init__(self, model):
        super().__init__(model)
        self.type = "|estd|"
        self.state = "explorando" #[(explorando), (saindo_zona_explorada), (retornando_base), (cooperando), (coletando_recurso)]
        self.destiny = None
        self.old_destinys = []
        
    '''Funcao de acao'''
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

            self.regist()
            print(f"\t> Estado de {self.type}_{self.unique_id}: {self.state}")
            #print(f"\t> celulas exploradas: {self.model.explored_cells}")
            
            #impressao do inventario do agente
            self.print_inventory()
            print()

    
    #def neighbors() permanece inalterada

    #def get_possible_steps() permanece inalterada

    #def colect_resources() permanece inalterada

    #def print_inventory() permanece inalterada

    #def print_inventory() permanece inalterada

    #def return_base() permanece inalterada

    #def deposite_inventory() permanece inalterada

    '''Função para definir o destino do agente'''
    def set_destiny(self):
        possible_destinys = self.model.explored_cells

        # Se o destino não estiver definido, definir o destino mais próximo
        if self.destiny is None:
            self.destiny = min(possible_destinys, key=lambda coord: math.dist(coord, self.pos))
            self.old_destinys.append(self.destiny)
            
        else: # o destino ja foi setado anteriormente
            # Filtra coordenadas que já foram exploradas
            possible_destinys = [coord for coord in possible_destinys if coord not in self.old_destinys]
            
            if possible_destinys:  # Verifica se ainda há destinos disponíveis
                self.destiny = min(possible_destinys, key=lambda coord: math.dist(coord, self.pos))
                self.old_destinys.append(self.destiny)


    '''Funcao para mover-se no mapa''' # alteracao de def move(): para levar em consideracao o conteudo registrado
    def move(self):
        possible_steps = self.get_possible_steps()
        if self.get_possible_steps(): #verifica se ha passos possiveis
            for new_position in possible_steps:
                #se ha uma possivel caminho que ainda nao foi explorado
                if not new_position in self.model.explored_cells:
                    self.state = "explorando"
                    self.model.grid.move_agent(self, new_position)
                    print(f"\t> {self.type}_{self.unique_id} moveu-se para {new_position}")
                    return True
                
            self.state = "saindo_zona_explorada"

            self.set_destiny()

            destiny_step = min(possible_steps, key=lambda coord: math.dist(coord, self.destiny)) #determina o passo a se seguir
            
            self.model.grid.move_agent(self, destiny_step)
            


        
