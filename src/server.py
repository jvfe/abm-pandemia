import tornado.web
from model.model import CovidModel, State, Common, Variant
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
        portrayal["Layer"] = 1
    elif agent.state == State.INFECTED:
        portrayal["Layer"] = 2
        portrayal["r"] = 0.7
        portrayal["Color"] = "#fc8d62"
    elif agent.state == State.EXPOSED:
        portrayal["Color"] = "#cc00cc"
        portrayal["Layer"] = 3
        portrayal["r"] = 0.6
    elif agent.state == State.RESISTANT:
        portrayal["Color"] = "#66c2a5"
        portrayal["Layer"] = 4
        portrayal["r"] = 0.4
    elif agent.state == State.DEAD:
        portrayal["Color"] = "#676767"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.4
    return portrayal


grid = CanvasGrid(agent_portrayal, 50, 50, 600, 600)
chart = LineChart(
    [
        {"Label": "Susceptible", "Color": "#8da0cb"},
        {"Label": "Exposed", "Color": "#cc00cc"},
        {"Label": "Infected", "Color": "#fc8d62"},
        {"Label": "Resistant", "Color": "#66c2a5"},
        {"Label": "Dead", "Color": "#676767"},
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
            2000,
            1,
            description="Choose how many susceptible agents to include in the model",
        ),
        "n_infected": UserSettableParameter(
            "slider",
            "Number of infected",
            3,
            1,
            2000,
            1,
            description="Choose how many infected agents to include in the model",
        ),
        "recovery_chance": UserSettableParameter(
            "slider",
            "Recovery chance",
            0.20,
            0.1,
            1,
            0.1,
        ),
        "resistance_chance": UserSettableParameter(
            "slider",
            "Resistance chance",
            0.01,
            0.01,
            1,
            0.05,
        ),
        "insert_variant": UserSettableParameter("checkbox", "With Variants", False),
    },
)
server.port = 8521