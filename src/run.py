from model.model import CovidModel
from mesa.batchrunner import BatchRunner
from server import server

model = CovidModel(997, 3, seed=1024)

# Rodar modelo por 10 iterações
for _ in range(10):
    model.step()


data = model.datacollector.get_model_vars_dataframe()

print(f"Rodando por 10 iterações:\n{data}")

server.launch(open_browser=False)
