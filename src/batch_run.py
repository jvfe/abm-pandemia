from model.model import CovidModel
from mesa.batchrunner import BatchRunner

modelo_normal = CovidModel(
    1500,
    3,
    spread_chance=0.2,
    fatality_rate=0.024,
    variation_chance=0.01,
    min_time_recovery=1,
    move_chance=0.5,
    insert_variant=False,
    width=60,
    height=60,
    seed=1024,
)

modelo_normal_lockdown = CovidModel(
    1500,
    3,
    spread_chance=0.2,
    fatality_rate=0.024,
    variation_chance=0.01,
    min_time_recovery=1,
    move_chance=0.25,
    insert_variant=False,
    width=60,
    height=60,
    seed=1024,
)

modelo_variante = CovidModel(
    1500,
    3,
    spread_chance=0.2,
    fatality_rate=0.024,
    variation_chance=0.01,
    min_time_recovery=1,
    move_chance=0.5,
    insert_variant=True,
    width=60,
    height=60,
    seed=1024,
)

modelo_variante_lockdown = CovidModel(
    1500,
    3,
    spread_chance=0.2,
    fatality_rate=0.024,
    variation_chance=0.01,
    min_time_recovery=1,
    move_chance=0.25,
    insert_variant=True,
    width=60,
    height=60,
    seed=1024,
)

print("Rodando modelo normal por 500 iterações")
for _ in range(500):
    modelo_normal.step()
    modelo_normal_lockdown.step()

data = modelo_normal.datacollector.get_model_vars_dataframe()

data_lockdown = modelo_normal_lockdown.datacollector.get_model_vars_dataframe()

data.to_csv("../data/modelo_comum.csv")
data_lockdown.to_csv("../data/modelo_comum_lockdown.csv")

print("Rodando modelo variante por 500 iterações")
for _ in range(500):
    modelo_variante.step()
    modelo_variante_lockdown.step()

data_variante = modelo_variante.datacollector.get_model_vars_dataframe()
data_variante_lockdown = (
    modelo_variante_lockdown.datacollector.get_model_vars_dataframe()
)

data_variante.to_csv("../data/modelo_variante.csv")
data_variante_lockdown.to_csv("../data/modelo_variante_lockdown.csv")


data_agentes_variante = modelo_variante.datacollector.get_agent_vars_dataframe()

data_agentes_variante.to_csv("../data/agentes_variante.csv")