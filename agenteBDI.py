import math
import mesa
import random
from agenteSimples import Reativo_Simples
from base import Base
from recurso import Recurso

class BDI(Reativo_Simples):
    def __init__(self, model):
        super().__init__(model)
        self.type = "[[@]]"

    '''Metodo de Acao'''
    def step(self):
        self.runStorm()

    '''Metodo para verificar se eh necessario retornar a base para fugir da tempestade'''
    def runStorm(self):
        for agent in self.model.schedule.agents:
            if isinstance(agent, Reativo_Simples) and agent != self:
                if self.calcDist(agent.pos, self.coords_base) >= self.model.clock_to_storm:
                    #aqui o bdi mandara o agente retornar a base
                    agent.state = "BDI_Ordenado"
                    self.return_agent_to_base(agent)
                    pass


    '''Metodo para retornar  agente para a base'''
    def return_agent_to_base(self,agent):
        base_neighborhood = self.model.grid.get_neighborhood(
            agent.coords_base,
            moore=True,
            include_center=False
        )

        # Se o agente não estiver na vizinhança da base
        if not agent.pos in base_neighborhood:
            possible_steps = agent.get_possible_steps() 
            if possible_steps: 
                next_coord = min(possible_steps, key=lambda coord: math.dist(coord, agent.coords_base)) 
                self.model.grid.move_agent(agent, next_coord) 
                return True

        return False

    '''Metodo calculo de distancia'''
    def calcDist(self,agent, base):
        distancia = math.sqrt((agent[0] - base[0])**2 + (agent[1] - base[1])**2)
        return distancia