import json
from mesa.visualization.ModularVisualization import VisualizationElement


class LineChart(VisualizationElement):

    package_includes = ["Chart.min.js"]
    local_includes = ["./visualization/LineChart.js"]

    def __init__(
        self,
        series,
        canvas_height=200,
        canvas_width=500,
        data_collector_name="datacollector",
    ):

        self.series = series
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.data_collector_name = data_collector_name

        series_json = json.dumps(self.series)
        new_element = f"new LineChart({series_json}, {canvas_width},  {canvas_height})"
        self.js_code = f"elements.push({new_element});"

    def render(self, model):
        current_values = []
        data_collector = getattr(model, self.data_collector_name)

        for s in self.series:
            name = s["Label"]
            try:
                val = data_collector.model_vars[name][-1]  # Latest value
            except (IndexError, KeyError):
                val = 0
            current_values.append(val)
        return current_values