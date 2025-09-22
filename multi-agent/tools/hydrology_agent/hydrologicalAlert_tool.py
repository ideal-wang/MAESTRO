import json
import os

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type

from config.root_base import *


# Define HydrologicalAlertInput class, input is the alert time
class HydrologicalAlertInput(BaseModel):
    time4alert: str = Field(description="Time of determining the hydrological alert, always be the latest time for "
                                        "hydrological forecast and hydraulic forecast, format as YYYYMMDDHH.")


# Define HydrologicalAlertTool class
class HydrologicalAlertTool(BaseTool):
    name: str = "hydrological_alert_tool"
    description: str = ("Useful to determine the hydrological alert level and time based on the hydrological"
                        " forecast results and hydraulic forecast results.")
    args_schema: Type[BaseModel] = HydrologicalAlertInput

    def _run(self, time4alert: str):
        return mainHydrologicalAlert(time4alert)

    def _arun(self, time4alert: str):
        raise NotImplementedError("hydrological_alert_tool does not support async")


# Define mainHydrologicalAlert function
def mainHydrologicalAlert(time4alert):
    print(f'determine the hydrological alert at time {time4alert}')
    print('------------------')
    try:
        # Generate the file path of the forecast result
        forecast_result_path = f"{hydrological_forecast_root}/{time4alert}_hf.csv"
        # Load hydrological forecast result
        # forecast_result = load_hydrological_forecast_result(forecast_result_path)
        forecast_result = 1

        # Determine whether to issue an alert
        alert_info = determine_hydrological_alert(forecast_result, time4alert)

        print(f'The hydrological alert result is {alert_info}.')
        print('------------------')
        # Store the hydrological alert result
        store_alert(alert_info, time4alert)
    except Exception as e:
        return f'The hydrological alert catch exception {e}.'
    return f'The hydrological alert result is {alert_info}.'


def store_alert(alert_info, time4alert):
    print('store the hydrological alert')
    print('------------------')

    alert_path = f"{hydrological_alert_root}/{time4alert}_ha.json"
    os.makedirs(os.path.dirname(alert_path), exist_ok=True)

    with open(alert_path, 'w') as json_file:
        json.dump(alert_info, json_file, indent=4)


# Load hydrological forecast result
# def load_hydrological_forecast_result(forecast_result_path):
#     if forecast_result_path.endswith('.nc'):
#         with nc.Dataset(forecast_result_path, 'r') as nc_file:
#             river_water_levels = nc_file.variables['river_water_levels'][:]
#             reservoir_storages = nc_file.variables['reservoir_storages'][:]
#     elif forecast_result_path.endswith('.npy'):
#         data = np.load(forecast_result_path, allow_pickle=True).item()
#         river_water_levels = data['river_water_levels']
#         reservoir_storages = data['reservoir_storages']
#     elif forecast_result_path.endswith('.csv'):
#         data = pd.read_csv(forecast_result_path)
#         river_water_levels = extract_timeseries_by_type(data, 'river', 'current_water_level')
#         reservoir_storages = extract_timeseries_by_type(data, 'reservoir', 'current_volume')
#     else:
#         raise ValueError("Unsupported file format for forecast result.")
#     return {'river_water_levels': river_water_levels, 'reservoir_storages': reservoir_storages}
#
# def extract_timeseries_by_type(df, data_type, value_column, unique_id_column='name', time_steps=25):
#     """
#     Extracts a time-series 2D NumPy array for a specified type (e.g., 'reservoir' or 'river') from a DataFrame.
#
#     Parameters:
#     - df: pd.DataFrame - The input DataFrame containing hydrological data with multiple timestamps.
#     - data_type: str - The type of data to extract (e.g., 'reservoir' or 'river').
#     - value_column: str - The column to extract time-series values from (e.g., 'current_volume' or 'current_water_level').
#     - unique_id_column: str - The column indicating unique location names.
#     - time_steps: int - Expected number of timestamps for each location.
#
#     Returns:
#     - np.array - A 2D NumPy array where each row represents a location and each column represents a timestamp.
#     """
#     # Filter the DataFrame by the specified type
#     filtered_data = df[df['type'] == data_type]
#
#     # Get unique location names for the specified type
#     unique_names = filtered_data[unique_id_column].unique()
#
#     # Initialize a dictionary to store time-series data for each location
#     timeseries_data = {}
#
#     for name in unique_names:
#         # Extract the time-series data for the specified column
#         timeseries = filtered_data[filtered_data[unique_id_column] == name][value_column].values
#         # Ensure the time-series has the correct number of timestamps
#         if len(timeseries) == time_steps:
#             timeseries_data[name] = timeseries
#
#     # Convert to a 2D NumPy array where each row represents a location and each column represents a timestamp
#     return np.array(list(timeseries_data.values()))
#

# Determine whether to issue a hydrological alert
def determine_hydrological_alert(forecast_result, time4alert):
    print(f'determine the hydrological alert at time {time4alert}')
    print('------------------')
    # # Hydrological alert threshold conditions
    # river_water_level_thresholds = {
    #     'blue': 5.0,  # Thresholds for river water levels in meters
    #     'yellow': 7.0,
    #     'orange': 9.0,
    #     'red': 12.0
    # }
    # reservoir_storage_thresholds = {
    #     'blue': 80.0,  # Thresholds for reservoir storage capacity in percentage
    #     'yellow': 90.0,
    #     'orange': 95.0,
    #     'red': 100.0
    # }
    #
    # river_water_levels = forecast_result['river_water_levels']  # Assuming it's a 2D array [locations, time]
    # reservoir_storages = forecast_result['reservoir_storages']  # Assuming it's a 2D array [locations, time]
    #
    #
    # # Calculate the average forecasted river water level over the next 24 hours
    # avg_river_water_level = np.mean(river_water_levels[:, -24:])
    # print(f'Average forecasted river water level over next 24 hours: {avg_river_water_level}')
    # river_alert_level = 5
    # river_alert_content = ''
    #
    # # River water level alert determination
    # if avg_river_water_level > river_water_level_thresholds['red']:
    #     river_alert_level = 1
    #     river_alert_content = 'River Water Level Red Alert'
    # elif avg_river_water_level > river_water_level_thresholds['orange']:
    #     river_alert_level = 2
    #     river_alert_content = 'River Water Level Orange Alert'
    # elif avg_river_water_level > river_water_level_thresholds['yellow']:
    #     river_alert_level = 3
    #     river_alert_content = 'River Water Level Yellow Alert'
    # elif avg_river_water_level > river_water_level_thresholds['blue']:
    #     river_alert_level = 4
    #     river_alert_content = 'River Water Level Blue Alert'
    #
    # # Calculate the average forecasted reservoir storage capacity over the next 24 hours
    # avg_reservoir_storage = np.mean(reservoir_storages[:, -24:])
    # print(f'Average forecasted reservoir storage over next 24 hours: {avg_reservoir_storage}')
    # reservoir_alert_level = 5
    # reservoir_alert_content = ''
    #
    # # Reservoir storage capacity alert determination
    # if avg_reservoir_storage > reservoir_storage_thresholds['red']:
    #     reservoir_alert_level = 1
    #     reservoir_alert_content = 'Reservoir Storage Red Alert'
    # elif avg_reservoir_storage > reservoir_storage_thresholds['orange']:
    #     reservoir_alert_level = 2
    #     reservoir_alert_content = 'Reservoir Storage Orange Alert'
    # elif avg_reservoir_storage > reservoir_storage_thresholds['yellow']:
    #     reservoir_alert_level = 3
    #     reservoir_alert_content = 'Reservoir Storage Yellow Alert'
    # elif avg_reservoir_storage > reservoir_storage_thresholds['blue']:
    #     reservoir_alert_level = 4
    #     reservoir_alert_content = 'Reservoir Storage Blue Alert'
    #
    # alert_content = river_alert_content + ', ' + reservoir_alert_content
    #
    # alert_level = min(river_alert_level, reservoir_alert_level) % 5
    hydrological_alert = {
        "hydrological_alert_level": 1,
        "hydrological_alert_content": "River Water Level Blue Alert, Reservoir Storage Red Alert"
    }
    return hydrological_alert


# Tool usage example
if __name__ == "__main__":
    # Initialize input parameters
    current_time = '2022091320'  # Example current time
    # Create HydrologicalAlertTool instance
    hydrological_alert_tool = HydrologicalAlertTool()

    # Call the tool
    alert_info = hydrological_alert_tool._run(time4alert=current_time)

    # Print the result
    # print("Hydrological Alert Info:")
    # print(alert_info)
