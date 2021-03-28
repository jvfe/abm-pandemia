from model.model import CovidModel
from mesa.batchrunner import BatchRunner

modelo_normal = CovidModel(
    1500, 3, insert_variant=False, width=60, height=60, seed=1024
)
modelo_variante = CovidModel(
    1500, 3, insert_variant=True, width=60, height=60, seed=1024
)

for _ in range(2000):
    modelo_normal.step()


data = modelo_normal.datacollector.get_model_vars_dataframe()

print(f"Rodando modelo normal por 2000 iterações:\n{data}")

data.to_csv("../data/modelo_comum_dados.csv")

for _ in range(2000):
    modelo_variante.step()

data_variante = modelo_variante.datacollector.get_model_vars_dataframe()
print(f"Rodando modelo variante por 2000 iterações:\n{data_variante}")

data_agentes_variante = modelo_variante.datacollector.get_agent_vars_dataframe()

data_variante.to_csv("../data/modelo_variante_dados.csv")
data_agentes_variante.to_csv("../data/agentes_variante.csv")