import json
import os
import numpy as np
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type

from config.root_base import *  # Ensure you have the appropriate paths in your config

class AgriculturalAlertInput(BaseModel):
    time4alert: str = Field(
        description="Time of determining the agricultural alert, always be the latest time for agricultural forecast, format as YYYYMMDDHH."
    )

class AgriculturalAlertTool(BaseTool):
    name: str = "agricultural_alert_tool"
    description: str = (
        "Useful to determine the agricultural alert level and time based on the agricultural forecast results."
    )
    args_schema: Type[BaseModel] = AgriculturalAlertInput

    def _run(self, time4alert: str):
        return mainAgriculturalAlert(time4alert)

    def _arun(self, time4alert: str):
        raise NotImplementedError("agricultural_alert_tool does not support async")


# Define mainAgriculturalAlert function
def mainAgriculturalAlert(time4alert):
    # Load agricultural forecast data
    forecast_result = load_forecast_result(time4alert)

    # Determine the agricultural alert
    alert_info = determine_alert(forecast_result, time4alert)

    # Store the agricultural alert result
    store_alert(alert_info, time4alert)

    return f'The agricultural alert is {alert_info}'

def store_alert(alert_info, time4alert):
    print('Store the agricultural alert')
    print('------------------')
    alert_path = f"{rural_alert_root}/{time4alert}_ra.json"
    os.makedirs(os.path.dirname(alert_path), exist_ok=True)

    with open(alert_path, 'w') as json_file:
        json.dump(alert_info, json_file, indent=4)

# Load agricultural forecast results
def load_forecast_result(time4alert):
    print('Load the agricultural forecast data')
    print('------------------')
    # Here we would typically load forecast data
    # forecast_result_path = f"{agricultural_forecast_root}/{time4alert}_af.npy"
    # forecast_result = np.load(forecast_result_path)
    forecast_result = 1  # Placeholder for actual forecast data
    return forecast_result

# Determine whether to issue an alert
def determine_alert(forecast_result, time4alert):
    print(f'Determine the agricultural alert at time {time4alert}')
    print('------------------')

    # Placeholder logic for determining the alert based on forecast result
    agricultural_alert = {
        "agricultural_alert_level": 2,
        "agricultural_alert_content": "Severe Flood Damage Orange Alert"
    }
    return agricultural_alert

# Tool invocation example
if __name__ == "__main__":
    agricultural_alert_tool = AgriculturalAlertTool()

    # Call the tool
    alert_info = agricultural_alert_tool._run(time4alert='2022091320')
    print(alert_info)
