import json
import os

import numpy as np
import time
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from config.root_base import *


class MeteorologicalAlertInput(BaseModel):
    time4alert: str = Field(description="Time of determining the meteorological alert, always be the latest time for "
                                        "meteorological forecast, format as YYYYMMDDHH.")


class MeteorologicalAlertTool(BaseTool):
    name: str = "meteorological_alert_tool"
    description: str = ("Useful to determine the meteorological alert level and time based on the meteorological "
                        "forecast results.")
    args_schema: Type[BaseModel] = MeteorologicalAlertInput

    def _run(self, time4alert: str):
        return mainMeteorologicalAlert(time4alert)

    def _arun(self, time4alert: str):
        raise NotImplementedError("weather_alert_tool does not support async")


# Define mainMeteorologicalAlert function
def mainMeteorologicalAlert(time4alert):

    # # load meteorological forecast data
    forecast_result = load_forecast_result(time4alert)
    #
    # # determine the meteorological alert
    alert_info = determine_alert(forecast_result, time4alert)
    # store the meteorological alert result
    store_alert(alert_info, time4alert)
    return f'The meteorological_alert is {alert_info}'

def store_alert(alert_info, time4alert):
    print('store the meteorological alert')
    print('------------------')
    alert_path = f"{meteorological_alert_root}/{time4alert}_ma.json"
    os.makedirs(os.path.dirname(alert_path), exist_ok=True)

    with open(alert_path, 'w') as json_file:
        json.dump(alert_info, json_file, indent=4)

# Load meteorological forecast results
def load_forecast_result(time4alert):
    print('load the forecast meteorological data')
    print('------------------')
    # forecast_result_path = f"{meteorological_forecast_root}/{time4alert}_mf.npy"
    # if forecast_result_path.endswith('.nc'):
    #     with nc.Dataset(forecast_result_path, 'r') as nc_file:
    #         forecast_result = nc_file.variables['Pr'][:]
    # elif forecast_result_path.endswith('.npy'):
    #     forecast_result = np.load(forecast_result_path)
    forecast_result = 1
    return forecast_result


# Determine whether to issue an alert
def determine_alert(forecast_result, time4alert):
    print(f'determine the meteorological alert at time {time4alert}')
    print('------------------')
    meteorological_alert = {
        "meteorological_alert_level": 2,
        "meteorological_alert_content": "Heavy Rain Orange Alert"
    }
    return meteorological_alert


# Tool invocation example
if __name__ == "__main__":
    weather_alert_tool = MeteorologicalAlertTool()

    # Call the tool
    alert_info = weather_alert_tool._run(time4alert='2022091320')

