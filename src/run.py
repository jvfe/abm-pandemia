# %%
from model.model import *
from mesa.batchrunner import BatchRunner

fixed_params = {"width": 10, "height": 10}
variable_params = {"N": range(10, 500, 10)}

batch_run = BatchRunner(
    MoneyModel,
    variable_params,
    fixed_params,
    iterations=5,
    max_steps=100,
    model_reporters={"Gini": compute_gini},
)
batch_run.run_all()

# %%
import matplotlib.pyplot as plt

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.Gini)
# %%
# Get the Agent DataCollection
data_collector_agents = batch_run.get_collector_agents()

data_collector_agents[(10, 2)]
# %%
# Get the Model DataCollection.

data_collector_model = batch_run.get_collector_model()

data_collector_model[(10, 1)]
