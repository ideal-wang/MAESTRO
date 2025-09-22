from datetime import datetime
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
import matplotlib.pyplot as plt
import numpy as np

from config.root_base import *



class MeteorologicalVisualizeInput(BaseModel):
    visualize_data_type: str = Field(
        description="The type of meteorological data to visualize. This could be 'temperature', 'precipitation', 'wind speed', etc."
    )
    location4visualize: str = Field(
        default="whole province",  # Default value for location is "whole province"
        description="The geographic location for which the meteorological data visualization is to be generated. It could be a city name, coordinates (latitude, longitude), or any location identifier."
    )
    time4visualize: str = Field(
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Default time is the current time
        description="The specific time or time range for which the meteorological data visualization is needed. It could be a timestamp or a date range (e.g., '2025-02-07' or '2025-02-01 to 2025-02-07')."
    )
    visualize_mode: str = Field(
        description="The mode of visualization. 'brief' for basic visualizations and 'professional' for detailed, professional visualizations."
    )





class MeteorologicalVisualizeTool(BaseTool):
    name: str = "meteorological_visualize_tool"
    description: str = (
        "Useful for visualizing meteorological data such as temperature, precipitation, wind speed, etc. "
        "Supports both basic and professional visualizations for a given location and time.")
    args_schema: Type[BaseModel] = MeteorologicalVisualizeInput

    def _run(self, visualize_data_type: str, location4visualize: str, time4visualize: str, visualize_mode: str):
        return mainMeteorologicalVisualize(visualize_data_type, location4visualize, time4visualize,
                                                  visualize_mode)

    def _arun(self, visualize_data_type: str, location4visualize: str, time4visualize: str, visualize_mode: str):
        raise NotImplementedError("meteorological_visualize_tool does not support async")
def mainMeteorologicalVisualize(visualize_data_type, location4visualize, time4visualize, visualize_mode):
    # Placeholder function for visualizing meteorological data
    print(f"Visualizing data of type '{visualize_data_type}' for location '{location4visualize}' "
          f"at time '{time4visualize}' in '{visualize_mode}' mode.")
    print("------------------")
    # Here you could add logic for generating different kinds of visualizations
    # based on the input parameters.
    if visualize_mode == "brief":
        print("Generating brief visualization...")
        # Example: simplified graph, basic chart, etc.
    elif visualize_mode == "professional":
        print("Generating professional visualization...")
        # Example: detailed chart, maps, overlays, etc.
    else:
        return "Invalid visualization mode."

    data = np.random.rand(10, 10)
    # plt.imshow(data, cmap='viridis')
    # plt.colorbar()
    # plt.title(f"{visualize_data_type}-{visualize_mode} Image")
    # plt.show()

    return f"Visualization for '{visualize_data_type}' data in '{visualize_mode}' mode completed."


if __name__ == '__main__':
    # Initialize input parameters
    visualize_data_type = 'temperature'  # Example: 'temperature', 'precipitation', etc.
    location = 'Ningbo city'  # Location for the visualization
    time4visualize = '2025-02-07 14:00:00'  # Time for which the data is to be visualized
    visualize_mode = 'brief'  # Mode could be 'brief' or 'professional'

    meteorological_visualize_tool = MeteorologicalVisualizeTool()

    # Call the tool
    visualization_result = meteorological_visualize_tool._run(visualize_data_type, location, time4visualize,
                                                              visualize_mode)

    # Print the result
    print(visualization_result)
