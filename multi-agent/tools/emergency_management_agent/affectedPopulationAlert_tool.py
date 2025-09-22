import json
import os

import numpy as np
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type

from config.root_base import *
# Define PopulationAlertInput class to input time of population impact assessment
class PopulationAlertInput(BaseModel):
    time4alert: str = Field(description="Time of determining the population alert, always be the latest time for "
                                        "affected population forecast, format as YYYYMMDDHH.")

# Define PopulationAlertTool class
class PopulationAlertTool(BaseTool):
    name: str = "population_alert_tool"
    description: str = "Useful to determine if a population alert should be issued based on the forecast affected population result"
    args_schema: Type[BaseModel] = PopulationAlertInput

    def _run(self, time4alert: str):
        return mainPopulationAlert(time4alert)

    def _arun(self, time4alert: str):
        raise NotImplementedError("population_alert_tool does not support async")

# Define mainPopulationAlert function
def mainPopulationAlert(time4alert):
    print(f'determine the population alert at time {time4alert}')
    # Generate the path of the impact assessment results
    impact_result_path = f"{affected_population_forecast_root}/{time4alert}_apf.npy"
    # Load impact assessment result
    impact_result = load_impact_result(impact_result_path)
    # Determine whether to initiate an alert
    alert_info = determine_population_alert(impact_result, time4alert)
    print(f"The population alert result is {alert_info}")
    print('------------------')

    store_alert(alert_info, time4alert)
    return f"The population alert result is {alert_info}"

def store_alert(alert_info, time4alert):

    print('store the meteorological alert')
    print('------------------')
    alert_path = f"{affected_population_alert_root}/{time4alert}_apa.json"
    os.makedirs(os.path.dirname(alert_path), exist_ok=True)
    with open(alert_path, 'w') as json_file:
        json.dump(alert_info, json_file, indent=4)
# Load impact assessment result
def load_impact_result(impact_result_path):
    print('load the forecast affected population data')
    print('------------------')
    # Load results assuming they are stored in numpy array format
    # ap_res = np.load(impact_result_path)
    ap_res = np.ones(5)
    return ap_res

# Determine whether to initiate a population alert
def determine_population_alert(impact_result, time4alert):

    # # Define threshold conditions for population alerts
    # ap_threshold = 5000         # Number of injured persons for an alert
    #
    # # Initialize alert info
    # alert_info = {
    #     'affectedpopulation_alert': {'alert_level': 0, 'alert_time': None}
    # }
    #
    # # Aggregate impact results
    # total_injured = np.sum(impact_result)
    #
    # # Injury alert check
    # if total_injured > ap_threshold:
    #     alert_info['affectedpopulation_alert']['alert_level'] = 1
    #     alert_info['affectedpopulation_alert']['alert_time'] = time4alert
    alert_info = {
        "affected_population_alert_level": 1,
        "affected_population_alert_content": "Population affected Red Alert"
    }
    return alert_info

# Example tool invocation
if __name__ == "__main__":
    # Create PopulationAlertTool instance
    population_alert_tool = PopulationAlertTool()
    # Call the tool
    alert_info = population_alert_tool._run(time4alert="2022091320")
    # print(alert_info)
