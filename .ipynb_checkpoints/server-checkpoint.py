from model import MoneyModel
import mesa
from mesa.visualization import SolaraViz, make_plot_component, make_space_component

def agent_portrayal(agent):
    return {
        "color": "tab: blue",
        "size":50,
    }

model_params = {
    "n": {
        "type": "SliderInt",
        "value": 50,
        "label": "Number of Agents",
        "min": 10,
        "max": 100,
        "step": 1,
    },
    "width": 10,
    "height": 10,
    }

# Criando instancia inicial de modelo

SpaceGraph = make_space_component(agent_portrayal)
GiniPlot = make_plot_component("Gini")

page = SolaraViz(
    components = [SpaceGraph, GiniPlot],
    model_params = model_params,
    name = "Boltzmann Wealth Model",
)

# Isso é requerido para renderizar a visualizacao no Jupyter notebook
page.render()