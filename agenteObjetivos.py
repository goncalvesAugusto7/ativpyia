import math
from agenteEstados import Baseado_Estados

class Baseado_Objetivos(Baseado_Estados):
    def __init__(self, model):
        super().__init__(model)
        self.type = "|objt|"


    '''Funcao de acao'''
    def step(self):
        print(f"-> AGENTE {self.__class__.__name__} {self.type}_{self.unique_id}__________________________________________________")
        
        if self.state != "cooperando" and self.state != "BDI_Ordenado":
                #primeiro, o agente deposita seus itens na base. E necessario estar na vizinhanca da base e ter itens no inventario
            if not self.deposite_inventory():
                #caso nao deposite, o agente verifica se ha itens para coletar em sua vizinhanca
                if self.resources_in_neighborhood() != True:
                    #se nao houver ele se move para outra celula
                    if not self.go_to_nearest_resource():
                        self.move()
                else: 
                    #se houver, ele coleta um item
                    self.collect_resources()
                    self.state = "retornando_base"
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
    
    def go_to_nearest_resource(self):
        # Verifica se o destino atual não é a posição atual
        if self.destiny != self.pos:
            # Verifica se há recursos encontrados
            if self.model.found_resources:
                
                # Filtra as opções da lista de recursos encontrados, excluindo aqueles com valor 50
                list_options = [pos for pos, vu in self.model.found_resources.items() if vu != 50]
                
                if list_options:
                    self.state = "atras_recurso"
                    print(f"Lista de opções: {list_options}")
                    
                    # Define o destino como a coordenada explorada mais próxima do agente
                    self.destiny = min(list_options, key=lambda coord: math.dist(coord, self.pos))
                    self.old_destinys.append(self.destiny)
                    
                    # Define o próximo passo em direção ao destino
                    destiny_step = min(self.get_possible_steps(), key=lambda coord: math.dist(coord, self.destiny))

                    if self.pos == self.destiny:
                        self.old_destinys.append(self.destiny)
                        possible_destinys = [cell for cell in self.model.explored_cells if cell not in self.old_destinys]
                        
                        # Atualiza o destino caso não tenha células inexploradas ao redor
                        if possible_destinys:
                            self.destiny = min(possible_destinys, key=lambda coord: math.dist(coord, self.pos))

                    # Move o agente para o próximo passo em direção ao destino
                    self.model.grid.move_agent(self, destiny_step)
                    return True
        
        self.destiny = None
        return False
            
            


        
