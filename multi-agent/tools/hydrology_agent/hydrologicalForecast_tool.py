import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from config.root_base import *

# Define the HydrologicalForecastInput class
class HydrologicalForecastInput(BaseModel):
    time4forecast: str = Field(description="Time of making the hydrological forecast, format as YYYYMMDDHH")
    forecast_duration: str = Field(description="Duration for hydrological forecast (e.g., '24h')")


# Define the HydrologicalForecastTool class
class HydrologicalForecastTool(BaseTool):
    name: str = "hydrological_forecast_tool"
    description: str = ("Useful to forecast hydrological data in the forecast duration based on past hydrological data "
                        "and meteorological forecast data")
    args_schema: Type[BaseModel] = HydrologicalForecastInput

    def _run(self, time4forecast: str, forecast_duration: str):
        return mainHydrologicalForecast(time4forecast, forecast_duration)

    def _arun(self, time4forecast: str, forecast_duration: str):
        raise NotImplementedError("hydrological_forecast_tool does not support async")

# Define the mainHydrologicalForecast function
def mainHydrologicalForecast(time4forecast, forecast_duration):
    print(f'Calculating the hydrological forecast data at time {time4forecast} for the future {forecast_duration}')
    print('-------------------')
    try:
        print('read the past data.')
        print('-------------------')
        print('load the forecast model and calculate the future data.')
        print('-------------------')
        print('store the forecast hydrological data')
        # past_meteorological_data_path = f'{meteorological_monitor_root}/{time4forecast}_mm.npy'
        # past_meteorological_data = np.load(past_meteorological_data_path)
        #
        forecast_time = (datetime.strptime(time4forecast, "%Y%m%d%H") + timedelta(hours=int(forecast_duration.rstrip('h')))).strftime(
            "%Y%m%d%H")
        forecast_result_path = f'{hydrological_forecast_root}/{forecast_time}_hf.npy'
        os.makedirs(os.path.dirname(forecast_result_path), exist_ok=True)

        forecast_hydraulic_result = np.ones(5)
        np.save(forecast_result_path, forecast_hydraulic_result)
    except Exception as e:
        return f"The hydrological forecast task is failed and the exception is {e}."

    return f"The hydrological forecast task has completed and the forecast data between {time4forecast} to {forecast_time} is calculated."

# Tool invocation example
if __name__ == "__main__":
    # Initialize input parameters
    current_time = '2022091320'
    forecast_duration = '24h'
    # Create an instance of HydrologicalForecastTool
    hydrological_forecast_tool = HydrologicalForecastTool()

    # Call the tool
    forecast_result = hydrological_forecast_tool._run(current_time, forecast_duration)

    # Print the result
    # print("Hydrological Forecast Result Path is :")
    # print(forecast_result)
