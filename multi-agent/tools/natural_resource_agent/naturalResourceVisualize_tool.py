from datetime import datetime
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
import matplotlib.pyplot as plt
import numpy as np

from config.root_base import *  # Ensure you have the appropriate config import

class NaturalResourceVisualizeInput(BaseModel):
    visualize_data_type: str = Field(
        description="The type of disaster-related natural resource data to visualize. This could be 'landslide impact', 'flood distribution', 'storm surge', 'coastal erosion', etc."
    )
    location4visualize: str = Field(
        default="whole province",  # Default value for location is "whole province"
        description="The geographic location for which the disaster-related natural resource data visualization is to be generated. It could be a city, region, or coordinates affected by a geological or marine disaster."
    )
    time4visualize: str = Field(
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Default to current time
        description="The specific time or time range for which the disaster data visualization is needed. It could be a timestamp or a date range."
    )
    visualization_mode: str = Field(
        default="brief",  # Default visualization mode is 'brief'
        description="The mode of visualization. Could be 'brief' for a high-level overview or 'professional' for more detailed and sophisticated visualizations."
    )


class NaturalResourceVisualizeTool(BaseTool):
    name: str = "natural_resource_visualize_tool"
    description: str = (
        "A tool for visualizing disaster-related natural resource data such as landslides, floods, storm surges, and coastal erosion. "
        "It supports both brief overviews and professional-level visualizations, allowing for a deeper understanding of disaster impacts."
    )
    args_schema: Type[BaseModel] = NaturalResourceVisualizeInput

    def _run(self, visualize_data_type: str, location4visualize: str, time4visualize: str, visualization_mode: str):
        return mainNaturalResourceVisualize(visualize_data_type, location4visualize, time4visualize, visualization_mode)

    def _arun(self, visualize_data_type: str, location4visualize: str, time4visualize: str, visualization_mode: str):
        raise NotImplementedError("natural_resource_visualize_tool does not support async operations.")

def mainNaturalResourceVisualize(visualize_data_type: str, location4visualize: str, time4visualize: str, visualization_mode: str):
    print(f"Visualizing data of type '{visualize_data_type}' for location '{location4visualize}' "
          f"at time '{time4visualize}' in '{visualization_mode}' mode.")
    
    # Example data, in practice, fetch the data from an API or database
    # data = np.random.random(10) * 100  # Placeholder data for visualization

    # # Set plot style based on visualization mode
    # if visualization_mode == "brief":
    #     plt.figure(figsize=(6, 4))
    #     plt.bar(range(len(data)), data)
    #     plt.title(f"Brief Overview: {visualize_data_type} in {location4visualize} at {time4visualize}")
    #     plt.xlabel("Index")
    #     plt.ylabel(f"{visualize_data_type} Value")
    # elif visualization_mode == "professional":
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(data, marker="o", linestyle='-', color='b')
    #     plt.title(f"Professional Visualization: {visualize_data_type} in {location4visualize} at {time4visualize}")
    #     plt.xlabel("Index")
    #     plt.ylabel(f"{visualize_data_type} Value")
    #     plt.grid(True)

    # plt.show()

    return f"Visualization for {visualize_data_type} in {location4visualize} at {time4visualize} has been generated in '{visualization_mode}' mode."


if __name__ == '__main__':
    # Initialize input parameters
    visualize_data_type = 'landslide impact'
    location = 'Coastal Region'
    time4visualize = '2025-03-01'
    visualize_mode = 'brief'

    natural_resource_visualize_tool = NaturalResourceVisualizeTool()

    # Call the tool
    visualize_result = natural_resource_visualize_tool._run(visualize_data_type, location, time4visualize, visualize_mode)

    # Print the result
    print(visualize_result)
