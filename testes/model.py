'''from mesa import Model
from agent import MoneyAgent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
import random

class MoneyModel(Model):
    # um modelo com alguns numeros de agentes

    def __init__(self, N, width, hight):
        self.num_agents = N
        self.grid = MultiGrid(width, hight, True)
        self.random = random.Random()
        self.schedule = RandomActivation(self)

        # Criar agentes
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

            # Adicionando o agente em uma celula aleatoria no grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        # Avanca a posicao do agente em um passo
        self.schedule.step()'''
