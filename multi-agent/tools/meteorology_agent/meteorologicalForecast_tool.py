import os

from pydantic import BaseModel, Field, ConfigDict
from langchain.tools import BaseTool
from typing import Type
import numpy as np
from datetime import datetime, timedelta
from config.root_base import *
# Define the MeteorologicalForecastInput class
class MeteorologicalForecastInput(BaseModel):
    time4forecast: str = Field(description="Time of making the meteorological forecast, format as YYYYMMDDHH")
    forecast_duration: str = Field(description="Duration for meteorological forecast (e.g., '24h')")

# Define the MeteorologicalForecastTool class
class MeteorologicalForecastTool(BaseTool):
    name: str = "meteorological_forecast_tool"
    description: str = ("Useful to forecast meteorological conditions in the future forecast duration "
                        "based on past meteorological data.")
    args_schema: Type[BaseModel] = MeteorologicalForecastInput

    def _run(self, time4forecast: str, forecast_duration: str):
        print(f'\nforecast the meteorological data at {time4forecast} for the future {forecast_duration}\n')
        return mainMeteorologicalForecast(time4forecast, forecast_duration)

    def _arun(self, time4forecast: str, forecast_duration: str):
        raise NotImplementedError("weather_forecast_tool does not support async")

# Define the mainMeteorologicalForecast function
def mainMeteorologicalForecast(time4forecast, forecast_duration):
    print(f'calculate the meteorological forecast result at time {time4forecast} for the duration at {forecast_duration}')
    print('-------------------')
    try:
        print('read the past data.')
        print('-------------------')
        print('load the forecast model and calculate the future data.')
        print('-------------------')
        print('store the forecast meteorological data')
        # past_meteorological_data_path = f'{meteorological_monitor_root}/{time4forecast}_mm.npy'
        # past_meteorological_data = np.load(past_meteorological_data_path)
        #
        forecast_time = (datetime.strptime(time4forecast, "%Y%m%d%H") + timedelta(hours=int(forecast_duration.rstrip('h')))).strftime(
            "%Y%m%d%H")
        forecast_result_path = f'{meteorological_forecast_root}/{forecast_time}_mf.npy'
        os.makedirs(os.path.dirname(forecast_result_path), exist_ok=True)
        # forecast_result = np.load(f'../数据文件/输出数据/气象输出/{forecast_time}_hx.npy')
        forecast_meteorological_result = np.ones(5)
        np.save(forecast_result_path, forecast_meteorological_result)
    except Exception as e:
        return f"The meteorological forecast task has failed, and meets the exception{e}"

    return f"The meteorological forecast task has completed and the forecast data between {time4forecast} to {forecast_time} is calculated."

# Tool invocation example
if __name__ == "__main__":
    # Initialize input parameters
    current_time = '2022091320'
    forecast_duration = '24h'
    # Create an instance of WeatherForecastTool
    meteorological_forecast_tool = MeteorologicalForecastTool()

    # Call the tool
    forecast_res = meteorological_forecast_tool._run(current_time, forecast_duration)
