    
    def step(self):
        print(f"-> AGENTE {self.__class__.__name__} {self.type}_{self.unique_id}__________________________________________________")
        print(f"\nBuddy: {self.buddy}; Coord_estrutura: {self.coord_estrutura}; Buddy_destiny: {self.buddy_destiny}; Destiny_estrutura: {self.destiny_estrutura}\n")

        #primeiro, ele tenta depositar a estrutura na base
        if (self.state != "atras_recurso" and self.state != "retornando_base") and not self.deposity_estrutura() :
            #caso nao consiga, procura por uma estrutura para carregar com um buddy
            if not self.move_to_estrutura():
                #se nao puder, faz os passos do agente baseado em objetivos
                if not self.deposite_inventory():
                    #caso nao deposite, o agente verifica se ha itens para coletar em sua vizinhanca
                    if self.resources_in_neighborhood() != True:
                        #se nao houver ele se move para outra celula
                        if not self.go_to_nearest_resource():
                            print(f"destino: {self.destiny}")
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

    '''Conjunto de métodos para analisar as estruturas antigas encontradas no mapa'''

    '''Função para verificar qual estrutura possui um agente por perto'''
    def analyse_estrutura_to_get(self):
        distance_self = 0   # distância do agente até estrutura
        distance_buddy = 0  # distância do colega agente até a estrutura
        possible_estruturas = {}  # armazena as estruturas e os agentes disponíveis mais próximos de cada uma
        chosen_estrutura = None
        agents = {}
        buddy_id = 0

        # Se houverem estruturas encontradas no mapa
        if self.model.found_estruturas:
            # Iterando sobre as estruturas para armazenar os dados
            for coord in self.model.found_estruturas:
                # Atualizando distance_self de cada estrutura
                distance_self = math.sqrt((self.pos[0] - coord[0])**2 + (self.pos[1] - coord[1])**2)  # distância euclidiana

                for agent in self.model.grid.agents:
                    if isinstance(agent, Reativo_Simples) and agent.pos != self.pos:  # verifica se o agente é um dos colegas e se ele não é o próprio cooperativo 
                        if len(agent.inventory) < 1:
                            # Se o agente disponível mais próximo da estrutura já está indo atrás de outro recurso, ele não é chamado
                            if not (isinstance(agent, Baseado_Objetivos) and agent.state == "atras_recurso"): 
                                distance_buddy = math.sqrt((agent.pos[0] - coord[0])**2 + (agent.pos[1] - coord[1])**2)  # distância euclidiana

                                possible_estruturas[coord] = distance_buddy + distance_self  # guarda a coordenada e a acessibilidade 
                                agents[coord] = agent.unique_id

            if possible_estruturas:  # verificando se há estruturas possíveis
                # Definindo a estrutura para ir atrás
                chosen_estrutura, _ = min(possible_estruturas.items(), key=lambda dist: dist[1])  # retorna a estrutura mais acessível
                buddy_id = agents[chosen_estrutura]

                print(f"\n>>>>>retorno de analyse_estrutura_to_get: {(chosen_estrutura, buddy_id)}\n")
                return (chosen_estrutura, buddy_id)
        
        return False

    '''Função para retornar o agente pelo seu id'''
    def get_buddy_by_id(self, id):
        for agent in self.model.schedule.agents:
            if agent.unique_id == id:
                return agent
        return None
    
    '''Função para pedir ajuda para agente colega'''
    def call_buddy(self):
        # Definindo a estrutura como destino do agente e seu colega chamado 
        if self.model.found_estruturas:
            result = self.analyse_estrutura_to_get()
            if not result:
                return False

            coords_estrutura, buddy_id = result
            self.buddy = self.get_buddy_by_id(buddy_id)
            self.coord_estrutura = coords_estrutura

            if self.buddy:  # se houver um buddy 
                # Vizinhanças do buddy e do agente
                buddy_neighborhood = self.model.grid.get_neighborhood(self.buddy.pos, moore=True, include_center=False)
                self_neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)

                # Definindo os destinos como a vizinhança da estrutura
                if buddy_neighborhood:
                    self.buddy_destiny = min(self.buddy.get_possible_steps(), key=lambda coord: math.dist(coord, self.coord_estrutura))
                if self_neighborhood:
                    self.destiny_estrutura = min(self.get_possible_steps(), key=lambda coord: math.dist(coord, self.coord_estrutura))

                # Definindo estados
                if hasattr(self.buddy, "state"):
                    self.buddy.state = "cooperando"
                self.state = "cooperando"

                print(f"\n>>>>> Saida de call_buddy: True\n")
                return True

        print(f"\n>>>>> Saida de call_buddy: False\n")
        return False

    '''Função para mover o agente e o buddy'''

    def move_to_estrutura(self):
        # verificando se o buddy já foi chamado
        if self.buddy:
            destiny_step_self = min(self.get_possible_steps(), key=lambda coord: math.dist(coord, self.destiny_estrutura))
            destiny_step_buddy = min(self.buddy.get_possible_steps(), key=lambda coord: math.dist(coord, self.buddy_destiny))

            # movendo o agente
            if self.destiny_estrutura != self.pos: #and not self.coord_estrutura in self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False):  # verificando se o agente já não alcançou
                print(f"Coop Moveu de {self.pos} para {destiny_step_self} com destino para {self.destiny_estrutura}")
                self.model.grid.move_agent(self, destiny_step_self)
                print(f"Coop estah em {self.pos}")
            # movendo o buddy
            if self.buddy_destiny != self.buddy.pos: #and not self.coord_estrutura in self.model.grid.get_neighborhood(self.buddy.pos, moore=True, include_center=False):  # verificando se o agente já não alcançou
                print(f"Buddy Moveu de {self.buddy.pos} para {destiny_step_buddy} com destino para {self.buddy_destiny}")
                self.model.grid.move_agent(self.buddy, destiny_step_buddy)
                print(f"Buddy estah em {self.buddy.pos}")

            print(f"***** Saida de move_to_estrutura: True")
            return True

        else:
            print(f"***** Saida de move_to_estrutura: False")
            self.call_buddy()
            

    '''Função para coletar a estrutura'''
    def collect_estrutura(self):
        # vizinhança da estrutura
        if len(self.inventory) == 0 and (self.buddy != None and self.coord_estrutura != None):
            estrutura = self.model.grid.get_cell_list_contents([self.coord_estrutura])

            if estrutura:  # Verifica se a estrutura está presente

                estrutura = estrutura[0]  # Obtém o primeiro (e provavelmente único) item na lista
                if (self.pos == self.destiny_estrutura) and (self.buddy.pos in self.buddy_destiny):
                    # adicionando no inventário
                    self.inventory.append(estrutura)
                    self.buddy.inventory.append(estrutura)

                    # removendo do found_resources
                    del self.model.found_resources[self.coord_estrutura]

                    # dados sobre a coleta
                    estrutura.collector = f"{self.type}_{self.unique_id} e {self.buddy.type}_{self.buddy.unique_id}"
                    self.collected_vu += 50
                    self.buddy.collected_vu += 50

                    # Move o agente para a posição do item
                    self.model.grid.move_agent(self, self.coord_estrutura)
                    self.model.grid.move_agent(self.buddy, self.coord_estrutura)

                    # imprimindo coleta
                    print(f"\t> {self.type}_{self.unique_id} coletou {estrutura.type}")
                    print(f"inventario do agente: {self.inventory}")

                    # removendo os itens coletados da grid
                    self.model.grid.remove_agent(estrutura)
                    self.model.schedule.remove(estrutura)

                    print(f"\n>>>>> Saida do collect_estrutura: True\n")
                    return True

                else:
                    self.move_to_estrutura()

        print(f"\n>>>>> Saida do collect_estrutura: False\t\tlen({self.inventory}) == 0 and {self.buddy} != None and {self.coord_estrutura} != None")
        return False

    '''Função para levar a estrutura até a base'''
    def return_base_with_estrutura(self):
        if self.buddy:
            self.return_base()
            self.model.grid.move_agent(self.buddy, self.pos)
            return True
        return False

    '''Função para depositar estrutura na base'''
    def deposity_estrutura(self):
        if len(self.inventory) > 0 and self.buddy != None and self.coord_estrutura != None:
            self_neighbors = self.neighbors()
            for neighbor in self_neighbors:
                if isinstance(neighbor, Base):
                    neighbor.storage.append(self.inventory[0])

                    print(f"\t >{self.inventory[0].type} depositado por {self.type}_{self.unique_id} e {self.buddy.type}_{self.buddy.unique_id}")

                    self.inventory.clear()
                    self.buddy.inventory.clear()
                    
                    if hasattr(self.buddy, "state"):
                        self.buddy.state = ""
                    self.state = ""

                    self.buddy = None
                    self.coord_estrutura = None
                    self.buddy_destiny = None
                    self.destiny_estrutura = None
                    
                    print(f"\n>>>>> Saida do deposity_estrutura: True\n")
                    return True

            self.return_base_with_estrutura()
        self.collect_estrutura()    
        print(f"\n>>>>> Saida do deposity_estrutura: False\n")
        return False
        
    '''Funcao para coletar estrutura'''
    def get_estrutura(self):
        pass
