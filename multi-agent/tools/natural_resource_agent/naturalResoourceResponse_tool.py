import json
import os
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type

from config.root_base import *


# Define the NaturalResourceResponseInput class
class NaturalResourceResponseInput(BaseModel):
    """
    Input schema for the NaturalResourceResponseTool.
    - time4response: The time for natural resource response suggestions in the format 'YYYYMMDDHH'.
                     This should always be the latest time for natural resource forecast.
    """
    time4response: str = Field(
        description="Time for natural resource response suggestions in format 'YYYYMMDDHH', always "
                    "is the latest time for natural resource forecast.")


# Define the NaturalResourceResponseTool class
class NaturalResourceResponseTool(BaseTool):
    """
    A tool to generate natural resource emergency response suggestions based on forecast and alert results.
    """
    name: str = "nature_resource_response_tool"
    description: str = ("Useful to generate natural resource emergency response suggestions based on nature resource "
                        "forecast results and natural resource alert results.")
    args_schema: Type[BaseModel] = NaturalResourceResponseInput

    def _run(self, time4response: str):
        return mainNaturalResourceResponse(time4response)

    def _arun(self, time4response: str):
        raise NotImplementedError("emergency_response_tool does not support async")


def mainNaturalResourceResponse(time4response: str):
    """
    Main function to generate and store natural resource emergency response suggestions.

    Args:
        time4response (str): The time for response suggestions in the format 'YYYYMMDDHH'.

    Returns:
        str: A string containing the generated response suggestion.
    """
    natural_resource_response = generate_emergency_response(time4response)

    store_suggestion(time4response, natural_resource_response)
    return f'meteorological response suggestion is {natural_resource_response}.'


def store_suggestion(time4response: str, natural_resource_response: dict):
    print('store the natural resource response')
    print('------------------')
    """
    Store the generated response suggestion to a JSON file.

    Args:
        time4response (str): The time for response suggestions in the format 'YYYYMMDDHH'.
        natural_resource_response (dict): The generated response suggestion.
    """
    suggestion_path = f"{natural_resource_response_root}/{time4response}_nrs.json"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(suggestion_path), exist_ok=True)

    with open(suggestion_path, 'w') as json_file:
        json.dump(natural_resource_response, json_file, indent=4)


def generate_emergency_response(time4response: str):
    """
    Generate natural resource emergency response suggestions based on the alert information.

    Args:
        time4response (str): The time for response suggestions in the format 'YYYYMMDDHH'.

    Returns:
        dict: A dictionary containing the response level and start time.
    """
    print(f'Generating natural resource emergency response suggestions at time {time4response}.')
    print('------------------')
    # # Initialize emergency response information
    # response_info = {
    #     'response_level': 'No Response',
    #     'response_start_time': 'None'
    # }

    # alert_path = f"{natural_resource_alert_root}/{time4response}_na.json"
    #
    # with open(alert_path, 'r') as json_file:
    #     alert_info = json.load(json_file)
    # alert_level = alert_info['natural_resource_alert_level']
    # alert_content = alert_info['natural_resource_alert_content']
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
    #
    # response_info['response_level'] = min(response_level, alert_level)

    response_info = {
        "response_level": 1,
        "response_start_time": "2022091608"
    }
    return response_info


# 示例使用
if __name__ == "__main__":
    tool = NaturalResourceResponseTool()

    # Call the tool
    res = tool._run(time4response='2022091420')

    print(res)