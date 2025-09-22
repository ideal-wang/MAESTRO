import json
import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from config.root_base import *


# Define the HydrologicalResponseInput class
class HydrologicalResponseInput(BaseModel):
    time4response: str = Field(description="The timestamp for generating hydrological response recommendations, "
                                           "formatted as 'YYYYMMDDHH'. This should always represent the most recent "
                                           "time point in the hydrological forecast.")


# Define the HydrologicalResponseTool class
class HydrologicalResponseTool(BaseTool):
    name: str = "hydrological_response_tool"
    description: str = ("Tool for generating emergency response recommendations based on hydrological forecasts and "
                        "alert status. It assesses potential risk levels using forecast data and predefined thresholds "
                        "to guide response planning.")
    args_schema: Type[BaseModel] = HydrologicalResponseInput

    def _run(self, time4response: str):
        return mainHydrologicalResponse(time4response)

    def _arun(self, alert_info: dict):
        raise NotImplementedError("hydrological_response_tool does not support async")


def mainHydrologicalResponse(time4response):
    hydrological_response = generate_emergency_response(time4response)

    store_suggestion(hydrological_response, time4response)
    return f'hydrological response suggestion is {hydrological_response}.'


def store_suggestion(hydrological_response, time4response):
    print('store the hydrological response')
    print('------------------')

    suggestion_path = f"{hydrological_response_root}/{time4response}_hrs.json"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(suggestion_path), exist_ok=True)

    with open(suggestion_path, 'w') as json_file:
        json.dump(hydrological_response, json_file, indent=4)


# Define the generate_emergency_response function
def generate_emergency_response(time4response):
    print(f'Generating hydrological emergency response suggestions at time {time4response}.')
    print('------------------')
    #
    # # Initialize emergency response information
    # response_info = {
    #     'response_level': 'No Response',
    #     'response_start_time': 'None'
    # }
    # forecast_result = pd.read_csv(f'{hydrological_forecast_root}/{time4response}_hf.csv')
    # alert_path = f"{hydrological_alert_root}/{time4response}_ha.json"
    #
    # with open(alert_path, 'r') as json_file:
    #     alert_info = json.load(json_file)
    # alert_level = alert_info['hydrological_alert_level']
    # alert_content = alert_info['hydrological_alert_content']
    #
    # # Initialize the response level
    # response_level = 5
    #
    # # If alert time exists, calculate the emergency response start time
    # if time4response:
    #     try:
    #         # Convert alert time string to datetime object
    #         alert_time = datetime.strptime(time4response, '%Y%m%d%H')
    #         # Calculate emergency response start time (12 hours after the alert time)
    #         response_start_time = alert_time + timedelta(hours=12)
    #         response_info['response_start_time'] = response_start_time.strftime('%Y%m%d%H')
    #     except ValueError:
    #         response_info['response_start_time'] = 'Invalid Time Format'
    #
    # main_river_water_level = forecast_result[forecast_result['name'] == 'Location_2']['current_water_level'].mean()
    # print(f'Average forecasted water level of the main river over next 24 hours: {main_river_water_level}')
    # alert_water_level = forecast_result[forecast_result['name'] == 'Location_2']['alert_water_level'].mean()
    # ensure_water_level = alert_water_level * 1.25
    #
    # # Generate emergency response level suggestions based on forecasted rainfall
    # if main_river_water_level > ensure_water_level:
    #     response_level = min(response_level, 1)
    # elif main_river_water_level > alert_water_level * 1.15:
    #     response_level = min(response_level, 2)
    # elif main_river_water_level > alert_water_level:
    #     response_level = min(response_level, 3)
    # elif alert_water_level > alert_water_level * 0.9:
    #     response_level = min(response_level, 4)
    #
    # # Generate emergency response level suggestions based on alert level
    # if alert_level == 1 or alert_level == 2:
    #     response_level = min(response_level, 2)
    # response_info['response_level'] = response_level % 5
    response_info = {
        "response_level": 1,
        "response_start_time": "2022091608"
    }
    return response_info

if __name__ == "__main__":
    tool = HydrologicalResponseTool()

    # Call the tool
    res = tool._run(time4response='2022091420')

    print(res)