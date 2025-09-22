import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from config.root_base import *  # Ensure paths are correctly defined in your config


# Define the AgriculturalForecastInput class
class AgriculturalForecastInput(BaseModel):
    time4forecast: str = Field(description="Time of making the agricultural forecast, format as YYYYMMDDHH")
    forecast_duration: str = Field(description="Duration for agricultural forecast (e.g., '24h')")


# Define the AgriculturalForecastTool class
class AgriculturalForecastTool(BaseTool):
    name: str = "agricultural_forecast_tool"
    description: str = ("Useful to forecast agricultural data in the forecast duration based on past agricultural data "
                        "and meteorological forecast data.")
    args_schema: Type[BaseModel] = AgriculturalForecastInput

    def _run(self, time4forecast: str, forecast_duration: str):
        return mainAgriculturalForecast(time4forecast, forecast_duration)

    def _arun(self, time4forecast: str, forecast_duration: str):
        raise NotImplementedError("agricultural_forecast_tool does not support async")


# Define the mainAgriculturalForecast function
def mainAgriculturalForecast(time4forecast, forecast_duration):
    print(f'Calculating the agricultural forecast data at time {time4forecast} for the future {forecast_duration}')
    print('-------------------')
    try:
        print('Read the past data.')
        print('-------------------')
        print('Load the forecast model and calculate the future data.')
        print('-------------------')
        print('Store the forecast agricultural data')

        # In practice, load real past agricultural and meteorological data
        # past_agricultural_data_path = f'{agricultural_monitor_root}/{time4forecast}_agri.npy'
        # past_agricultural_data = np.load(past_agricultural_data_path)

        # Calculate the forecast time based on the provided duration
        forecast_time = (datetime.strptime(time4forecast, "%Y%m%d%H") + timedelta(
            hours=int(forecast_duration.rstrip('h')))).strftime("%Y%m%d%H")

        forecast_result_path = f'{rural_forecast_root}/{forecast_time}_rf.npy'
        os.makedirs(os.path.dirname(forecast_result_path), exist_ok=True)

        forecast_agricultural_result = np.ones(5)  # Placeholder for forecast results (e.g., crop yields)
        np.save(forecast_result_path, forecast_agricultural_result)

    except Exception as e:
        return f"The agricultural forecast task failed and the exception is {e}."

    return f"The agricultural forecast task has completed and the forecast data between {time4forecast} to {forecast_time} is calculated."


# Tool invocation example
if __name__ == "__main__":
    # Initialize input parameters
    current_time = '2022091320'  # Example current time
    forecast_duration = '24h'  # Forecast duration (can be '24h', '48h', etc.)

    # Create an instance of AgriculturalForecastTool
    agricultural_forecast_tool = AgriculturalForecastTool()

    # Call the tool
    forecast_result = agricultural_forecast_tool._run(current_time, forecast_duration)
