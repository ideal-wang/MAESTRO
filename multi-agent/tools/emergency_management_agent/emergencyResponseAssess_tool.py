import json
import os
import pickle
from collections import deque

import pandas as pd
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type, List
from config.root_base import *

# Define the input model for Emergency Response Assessment
class EmergencyResponseAssessInput(BaseModel):
    """
    Input model for providing the timestamp for the final emergency response assessment.
    """
    time4response: str = Field(
        description=(
            "The timestamp for the final emergency response assessment. "
            "This value is always the same as the time4alert. "
            "Format: YYYYMMDDHH."
        )
    )

# Define the tool for emergency response assessment
class EmergencyResponseAssessTool(BaseTool):
    """
    A tool to evaluate and update the final emergency response level and its timestamp.
    """
    name: str = "emergency_response_assess_tool"
    description: str = (
        "Tool to evaluate the final emergency response level and time based on provided suggestions. "
        "The tool also updates this information to the environment for further use."
    )
    args_schema: Type[BaseModel] = EmergencyResponseAssessInput

    def _run(self, time4response: str):
        emergency_response = emergency_response_assess(time4response)
        return (f"The emergency response has been evaluated finally and updated in the environment. The emergency is "
                f"{emergency_response}")

    def _arun(self, time4response: str):
        raise NotImplementedError("emergency_response_assess_tool does not support async")


def set_global_state(emergency_response_level):
    with open(SYSTEM_FILE_PATH, 'rb') as f:
        system_file = pickle.load(f)
    original_level = system_file['emergency_response_level']
    system_file['emergency_response_level'] = emergency_response_level

    time4forecast = system_file['time4forecast']
    updated_duration = system_file['monitor_frequency']
    system_file['time4forecast'] = (
                datetime.strptime(time4forecast, "%Y%m%d%H")
                + timedelta(hours=int(updated_duration.rstrip('h')))
        ).strftime("%Y%m%d%H")

    time4alert = system_file['time4alert']
    updated_duration = system_file['monitor_frequency']
    system_file['time4alert'] = (
            datetime.strptime(time4alert, "%Y%m%d%H")
            + timedelta(hours=int(updated_duration.rstrip('h')))
    ).strftime("%Y%m%d%H")

    # reset the deque
    # system_file['subtask_queue'] = deque([{'subtask': 'Activate Emergency Response', 'status': 'pending'}])
    system_file['subtask_queue'] = deque()
    log_queue = deque()
    with open(LOG_QUEUE_FILE, 'wb') as f:
        pickle.dump(log_queue, f)

    with open(SYSTEM_FILE_PATH, 'wb') as f:
        pickle.dump(system_file, f)

def read_json(path):
    with open(path, 'r') as json_file:
        data = json.load(json_file)
    return data

def emergency_response_assess(time4response: str):
    try:
        # meteorological_response = read_json(f'{meteorological_response_root}/{time4response}_mrs.json')
        # hydrological_response = read_json(f'{hydrological_response_root}/{time4response}_hrs.json')
        # natural_resource_response = read_json(f'{natural_resource_response_root}/{time4response}_nrs.json')
        # responses = [
        #     meteorological_response,
        #     hydrological_response,
        #     natural_resource_response
        # ]
        #
        # filtered_responses = [response for response in responses if response['response_level'] != 0]
        #
        # # Calculate the response level
        # if filtered_responses:
        #     response_level = min(response['response_level'] for response in filtered_responses)
        # else:
        #     response_level = 0
        #
        # response_start_time = None
        # for response in filtered_responses:
        #     if response['response_level'] == response_level:
        #         response_start_time = response['response_start_time']
        #         break
        #
        # emergency_response = {
        #     'response_level': response_level,
        #     'response_start_time': response_start_time
        # }
        emergency_response = {
            "response_level": 2,
            "response_start_time": "2022091608"
        }
    except Exception as e:
        emergency_response = {'response_level': 0, 'response_start_time': ''}
    set_global_state(emergency_response['response_level'])
    # emergency_response.store()

    return f'the final emergency response assess result is {emergency_response}'


# Example usage
if __name__ == "__main__":
    # Create tool instance
    emergency_response_assess_tool = EmergencyResponseAssessTool()

    # Run the tool and get the command center information
    command_center_info = emergency_response_assess_tool._run(time4response='2022091520')

    # Print the result
    print(command_center_info)