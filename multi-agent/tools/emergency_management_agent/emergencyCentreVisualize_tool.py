from datetime import datetime
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
import matplotlib.pyplot as plt
import numpy as np

from config.root_base import *  # Ensure paths are correctly configured in your project


# Define the input schema for the EmergencyCenterVisualizationTool
class EmergencyCenterVisualizeInput(BaseModel):
    visualize_data_type: str = Field(
        description="The type of emergency data to visualize. This could be 'affected population', 'shelter resources', 'shelter capacity', etc."
    )
    location4visualize: str = Field(
        default="whole province",  # Default value for location is "whole province"
        description="The geographic location for which the emergency center data visualization is to be generated. It could be a city name, coordinates (latitude, longitude), or any location identifier."
    )
    time4visualize: str = Field(
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Default time is the current time
        description="The specific time or time range for which the emergency data visualization is needed. It could be a timestamp or a date range (e.g., '2025-02-07' or '2025-02-01 to 2025-02-07')."
    )
    visualize_mode: str = Field(
        description="The mode of visualization. 'brief' for basic visualizations and 'professional' for detailed, professional visualizations."
    )


# Define the EmergencyCenterVisualizationTool class
class EmergencyCenterVisualizationTool(BaseTool):
    name: str = "emergency_center_visualize_tool"
    description: str = (
        "Useful for visualizing emergency center data such as affected population, shelter resources, and shelter capacity. "
        "Supports both basic and professional visualizations for a given location and time."
    )
    args_schema: Type[BaseModel] = EmergencyCenterVisualizeInput

    def _run(self, visualize_data_type: str, location4visualize: str, time4visualize: str, visualize_mode: str):
        return mainEmergencyCenterVisualize(visualize_data_type, location4visualize, time4visualize, visualize_mode)

    def _arun(self, visualize_data_type: str, location4visualize: str, time4visualize: str, visualize_mode: str):
        raise NotImplementedError("emergency_center_visualize_tool does not support async")


# Define the main function to visualize emergency center data
def mainEmergencyCenterVisualize(visualize_data_type, location4visualize, time4visualize, visualize_mode):
    # Placeholder function for visualizing emergency center data
    print(f"Visualizing data of type '{visualize_data_type}' for location '{location4visualize}' "
          f"at time '{time4visualize}' in '{visualize_mode}' mode.")
    print("------------------")

    # Logic to generate the visualizations
    if visualize_mode == "brief":
        print("Generating brief visualization...")
        # Example: simplified graph, basic chart, etc.
    elif visualize_mode == "professional":
        print("Generating professional visualization...")
        # Example: detailed chart, maps, overlays, etc.
    else:
        return "Invalid visualization mode."

    # Simulate emergency center data (e.g., affected population and shelter resources)
    if visualize_data_type == "affected population":
        data = np.random.rand(10, 10) * 1000  # Simulated affected population data
    elif visualize_data_type == "shelter capacity":
        data = np.random.rand(10, 10) * 500  # Simulated shelter capacity data
    else:
        data = np.random.rand(10, 10) * 200  # Simulated shelter resources (e.g., supplies)

    # plt.imshow(data, cmap='YlOrRd')  # Using a 'YlOrRd' colormap for emergency data visualization
    # plt.colorbar()
    # plt.title(f"{visualize_data_type}-{visualize_mode} Visualization")
    # plt.show()

    return f"Visualization for '{visualize_data_type}' data in '{visualize_mode}' mode completed."


# Tool invocation example
if __name__ == '__main__':
    # Initialize input parameters
    visualize_data_type = 'affected population'  # Example: 'affected population', 'shelter capacity', etc.
    location = 'Ningbo city'  # Location for the visualization
    time4visualize = '2025-02-07 14:00:00'  # Time for which the data is to be visualized
    visualize_mode = 'brief'  # Mode could be 'brief' or 'professional'

    emergency_center_visualize_tool = EmergencyCenterVisualizationTool()

    # Call the tool
    visualization_result = emergency_center_visualize_tool._run(visualize_data_type, location, time4visualize,
                                                                visualize_mode)

    # Print the result
    print(visualization_result)
