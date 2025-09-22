import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import geopandas as gpd
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type

from config.root_base import *


# Define NaturalResourceForecastInput class
class NaturalResourceForecastInput(BaseModel):
    time4forecast: str = Field(description="The timestamp for generating the natural resource forecast, "
                                           "formatted as 'YYYYMMDDHH'.")
    forecast_duration: str = Field(description="The forecast period into the future (e.g., '24h').")


# Define NaturalResourceForecastTool class
class NaturalResourceForecastTool(BaseTool):
    name: str = "natural_resource_forecast_tool"
    description: str = (
        "Generates forecasts for natural resource hazards such as storm surges, ocean waves, and geological events. "
        "This tool leverages historical data over a specified duration to anticipate potential impacts, aiding in "
        "risk management, emergency preparedness, and resource allocation."
    )
    args_schema: Type[BaseModel] = NaturalResourceForecastInput

    def _run(self, time4forecast: str, forecast_duration: str):
        return mainNaturalResourceForecast(time4forecast, forecast_duration)

    def _arun(self, time4forecast: str, forecast_duration: str):
        raise NotImplementedError("natural_resource_forecast_tool does not support async")


# Define mainNaturalResourceForecast function
def mainNaturalResourceForecast(time4forecast, forecast_duration):
    print(f'calculate the natural resource forecast result at time {time4forecast} for the duration at {forecast_duration}')
    print('-------------------')
    try:
        print('read the past data.')
        print('-------------------')
        print('load the forecast model and calculate the future data.')
        print('-------------------')
        print('store the forecast natural resource data')
        # past_meteorological_data_path = f'{meteorological_monitor_root}/{time4forecast}_mm.npy'
        # past_meteorological_data = np.load(past_meteorological_data_path)
        #
        forecast_time = (datetime.strptime(time4forecast, "%Y%m%d%H") + timedelta(hours=int(forecast_duration.rstrip('h')))).strftime(
            "%Y%m%d%H")
        forecast_result_path = f'{natural_resource_forecast_root}/{forecast_time}_nf.npy'
        os.makedirs(os.path.dirname(forecast_result_path), exist_ok=True)

        forecast_natural_result = np.ones(5)
        np.save(forecast_result_path, forecast_natural_result)
    except Exception as e:
        return f"The natural resource forecast task has failed, and meets the exception{e}"

    return f"The natural resource forecast task has completed and the forecast data between {time4forecast} to {forecast_time} is calculated."

# Example usage of the tool
if __name__ == "__main__":
    # Initialize input parameters
    current_time = '2022091320'
    forecast_duration = '24h'
    # Create NaturalResourceForecastTool instance
    natural_resource_forecast_tool = NaturalResourceForecastTool()

    # Call the tool
    forecast_results = natural_resource_forecast_tool._run(current_time, forecast_duration)

    # # Print the result paths
    # print("Natural Resource Forecast Results Paths:")
    # print(forecast_results)
