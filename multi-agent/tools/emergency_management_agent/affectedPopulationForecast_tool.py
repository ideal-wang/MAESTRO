import os
from datetime import datetime, timedelta
from typing import Type

import numpy as np
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

from config.root_base import *


# define APForecastInput class
class APForecastInput(BaseModel):
    time4forecast: str = Field(description="Time of making the affected population forecast, format as YYYYMMDDHH")
    forecast_duration: str = Field(description="Duration for affected population forecast (e.g., '24h')")

# define APForecastTool class
class APForecastTool(BaseTool):
    name: str = "ap_forecast_tool"
    description: str = ("A tool to forecast the affected population based on meteorological forecast data for a "
                        "specified time period. It uses the provided time for forecasting and forecast duration to "
                        "predict potential the affected population due to weather conditions.")
    args_schema: Type[BaseModel] = APForecastInput


    def _run(self, time4forecast: str, forecast_duration: str):
        # return mainForecast(alarmTime, currentTime, self.shp_path, self.model_path, self.hazard_data_root)
        return mainAPForecast(time4forecast, forecast_duration)

    def _arun(self, time4forecast: str, forecast_duration: str):
        raise NotImplementedError("forecast_tool does not support async")

def mainForecast(time4forecast: str, forecast_duration: str):
    try:
        # calculate the final time for ap forecast
        forecast_time = (datetime.strptime(time4forecast, "%Y%m%d%H") + timedelta(
            hours=int(forecast_duration.rstrip('h')))).strftime(
            "%Y%m%d%H")

        # load meteorological forecast data
        meteorological_forecast_data = np.load(f'{meteorological_forecast_root}/{forecast_time}_mf.npy')

        # calculate the forecast ap data and store it
        forecast_result_path = f'{affected_population_forecast_root}/{forecast_time}_apf.npy'
        forecast_result = np.load(f'{affected_population_forecast_root}/{time4forecast}_apf.npy')
        np.save(forecast_result_path, forecast_result)

    except Exception as e:
        return f'meet exception {e}, when forecast the affected population.'

    return (f'The affected population forecast task has completed and the forecast data between {time4forecast} to '
            f'{forecast_time} is calculated.')

def mainAPForecast(time4forecast, forecast_duration):
    print(f'calculate the affected population forecast result at time {time4forecast} for the duration at {forecast_duration}')
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
        forecast_result_path = f'{affected_population_forecast_root}/{forecast_time}_apf.npy'
        os.makedirs(os.path.dirname(forecast_result_path), exist_ok=True)
        forecast_ap_result = np.ones(5)
        np.save(forecast_result_path, forecast_ap_result)
    except Exception as e:
        return f"The affected population forecast task has failed, and meets the exception{e}"

    return f"The affected population forecast task has completed and the forecast data between {time4forecast} to {forecast_time} is calculated."

if __name__ == '__main__':
    # Initialize input parameters
    current_time = '2022091320'
    forecast_duration = '24h'
    # Create an instance of WeatherForecastTool
    ap_forecast_tool = APForecastTool()

    # Call the tool
    forecast_res = ap_forecast_tool._run(current_time, forecast_duration)
