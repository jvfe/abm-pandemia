from model.model import CovidModel
from mesa.batchrunner import BatchRunner

# from server import server

modelo_normal = CovidModel(1200, 3, seed=1024)
modelo_variante = CovidModel(1200, 3, seed=1024)

for _ in range(2000):
    modelo_normal.step()


data = modelo_normal.datacollector.get_model_vars_dataframe()

print(f"Rodando modelo normal por 2000 iterações:\n{data}")

data.to_csv("../data/modelo_comum_dados.csv")

for _ in range(2000):
    modelo_variante.step()

data_variante = modelo_variante.datacollector.get_model_vars_dataframe()

print(f"Rodando modelo normal por 2000 iterações:\n{data_variante}")

data_variante.to_csv("../data/modelo_variante_dados.csv")

# server.launch(open_browser=False)
