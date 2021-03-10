# %%
from model.model import CovidModel
from mesa.batchrunner import BatchRunner

# fixed_params = {"width": 10, "height": 10}
# variable_params = {"N": range(10, 500, 10)}

model = CovidModel(997, 1)
for i in range(10):
    model.step()


model.datacollector.get_model_vars_dataframe()

# batch_run = BatchRunner(
#     CovidModel,
#     variable_params,
#     fixed_params,
#     iterations=5,
#     max_steps=100,
#     model_reporters={"Gini": compute_gini},
# )
# batch_run.run_all()
