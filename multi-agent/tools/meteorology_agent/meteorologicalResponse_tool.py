import json
import os
from datetime import datetime, timedelta

import numpy as np
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type



from config.root_base import *


# Define the MeteorologicalResponseInput class
class MeteorologicalResponseInput(BaseModel):
    time4response: str = Field(description="Time for meteorological response suggestions in format 'YYYYMMDDHH', always "
                                           "is the latest time for meteorological forecast.")

# Define the MeteorologicalResponseTool class
class MeteorologicalResponseTool(BaseTool):
    name: str = "meteorological_response_tool"
    description: str = ("Useful to generate meteorological emergency response suggestions based on meteorological "
                        "forecast and alert results.")
    args_schema: Type[BaseModel] = MeteorologicalResponseInput

    def _run(self, time4response: str):
        return mainMeteorologicalResponse(time4response)

    def _arun(self, time4response: str):
        raise NotImplementedError("emergency_response_tool does not support async")


def mainMeteorologicalResponse(time4response):
    meteorological_response = generate_emergency_response(time4response)
    # meteorological_response = {
    #     'response_level': 'Level I',
    #     'response_start_time': '2022091308'
    # }
    store_suggestion(meteorological_response, time4response)
    return f'meteorological response suggestion is {meteorological_response}.'


def store_suggestion(meteorological_response, time4response):
    print('store the meteorological response')
    print('------------------')
    suggestion_path = f"{meteorological_response_root}/{time4response}_mrs.json"
    # print(suggestion_path)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(suggestion_path), exist_ok=True)

    # Write the response to the JSON file
    with open(suggestion_path, 'w') as json_file:  # 'w' is typically used for writing text files
        json.dump(meteorological_response, json_file, indent=4)

# Define the generate_emergency_response function
def generate_emergency_response(time4response: str):
    print(f'Generating meteorological emergency response suggestions at time {time4response}.')
    print('------------------')
    # # Initialize emergency response information
    # response_info = {
    #     'response_level': 'No Response',
    #     'response_start_time': 'None'
    # }
    # forecast_result = np.load(f'{meteorological_forecast_root}/{time4response}_mf.npy')
    # alert_path = f"{meteorological_alert_root}/{time4response}_ma.json"
    #
    # with open(alert_path, 'r') as json_file:
    #     alert_info = json.load(json_file)
    # alert_level = alert_info['meteorological_alert_level']
    # alert_content = alert_info['meteorological_alert_content']
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
    # # Generate emergency response level suggestions based on forecasted rainfall
    # time_length = forecast_result.shape[1]
    # precipitation_result = forecast_result[:, time_length - 24:time_length]
    # precipitation_amount = np.partition(precipitation_result[:, -1], -2)[-2]
    # precipitation_thresholds = {
    #     'blue': 50.0,  # Blue alert for heavy rain
    #     'yellow': 80.0,  # Yellow alert for heavy rain
    #     'orange': 100.0,  # Orange alert for heavy rain
    #     'red': 150.0  # Red alert for heavy rain
    # }
    # if precipitation_amount > precipitation_thresholds['red']:
    #     response_level = min(response_level, 1)
    # elif precipitation_amount > precipitation_thresholds['orange']:
    #     response_level = min(response_level, 2)
    # elif precipitation_amount > precipitation_thresholds['yellow']:
    #     response_level = min(response_level, 3)
    # elif precipitation_amount > precipitation_thresholds['blue']:
    #     response_level = min(response_level, 4)
    #
    # # Generate emergency response level suggestions based on alert level
    # if alert_level == 1 or alert_level == 2:
    #     response_level = min(response_level, 2)
    # response_info['response_level'] = response_level % 5

    response_info = {
        'response_level': 'Level I',
        'response_start_time': '2022091308'
    }
    return response_info

# Example usage
if __name__ == "__main__":
    # Example alert information
    example_alert_info = {
        'alert_level': 'High Temperature Red Alert',
        'alert_time': '2022091308'
    }

    # Create an instance of the tool
    emergency_response_tool = MeteorologicalResponseTool()

    # Run the tool and get emergency response suggestions
    response_info = emergency_response_tool._run(example_alert_info['alert_time'])

    # Print the results
    print(response_info)
