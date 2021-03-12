import tornado.web
from model.model import CovidModel, State
from visualization.LineChart import LineChart
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 1,
    }

    if agent.state == State.SUSCEPTIBLE:
        portrayal["Color"] = "#8da0cb"
        portrayal["Layer"] = 0
    elif agent.state == State.INFECTED:
        portrayal["Color"] = "#fc8d62"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.6
    elif agent.state == State.RESISTANT:
        portrayal["Color"] = "#66c2a5"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5
    return portrayal


grid = CanvasGrid(agent_portrayal, 50, 50, 600, 600)
chart = LineChart(
    [
        {"Label": "Susceptible", "Color": "#8da0cb"},
        {"Label": "Infected", "Color": "#fc8d62"},
        {"Label": "Resistant", "Color": "#66c2a5"},
    ],
    data_collector_name="datacollector",
)


server = ModularServer(
    CovidModel,
    [grid, chart],
    "Agent-based pandemics simulation",
    {
        "n_susceptible": UserSettableParameter(
            "slider",
            "Number of susceptible",
            997,
            500,
            1200,
            1,
            description="Choose how many susceptible agents to include in the model",
        ),
        "n_infected": UserSettableParameter(
            "slider",
            "Number of infected",
            3,
            1,
            1200,
            1,
            description="Choose how many infected agents to include in the model",
        ),
        "virus_spread_chance": UserSettableParameter(
            "slider",
            "Viral spread chance",
            0.4,
            0.1,
            1,
            0.05,
        ),
        "recovery_chance": UserSettableParameter(
            "slider",
            "Recovery chance",
            0.04,
            0.01,
            1,
            0.05,
        ),
        "resistance_chance": UserSettableParameter(
            "slider",
            "Resistance chance",
            0.005,
            0.005,
            1,
            0.05,
        ),
    },
)
server.port = 8521