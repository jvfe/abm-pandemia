from model.model import CovidModel, State
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 1,
    }

    if agent.state == State.SUSCEPTIBLE:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
    elif agent.state == State.INFECTED:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.6
    elif agent.state == State.RESISTANT:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
    return portrayal


grid = CanvasGrid(agent_portrayal, 50, 50, 600, 600)
chart = ChartModule(
    [
        {"Label": "Susceptible", "Color": "Blue"},
        {"Label": "Infected", "Color": "Red"},
        {"Label": "Resistant", "Color": "Green"},
    ],
    data_collector_name="datacollector",
)
server = ModularServer(
    CovidModel,
    [grid, chart],
    "ABM Pandemics Model",
    {"n_susceptible": 997, "n_infected": 3},
)
server.port = 8521
server.launch()