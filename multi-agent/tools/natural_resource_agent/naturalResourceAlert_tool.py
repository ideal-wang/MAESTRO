import json
import os

import numpy as np
import time

import pandas as pd
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type

from config.root_base import *

# Define the NaturalResourceAlertInput class, with the input being the alert time
class NaturalResourceAlertInput(BaseModel):
    time4alert: str = Field(description="Time of determining the natural resource alert, always be the latest time "
                                          "for natural resource hazards forecast, format as YYYYMMDDHH.")

# Define the NaturalResourceAlertTool class
class NaturalResourceAlertTool(BaseTool):
    name: str = "natural_resource_alert_tool"
    description: str = ("Useful to determine the natural resource alert level and time based on the natural resource"
                        " forecast results.")
    args_schema: Type[BaseModel] = NaturalResourceAlertInput

    def _run(self, time4alert: str):
        return main_natural_resource_alert(time4alert)

    def _arun(self, time4alert: str):
        raise NotImplementedError("natural_resource_alert_tool does not support async")

# Main function for natural resource alert
def main_natural_resource_alert(time4alert):

    # # Load the natural resource forecast results
    # forecast_result_path = f"{natural_resource_forecast_root}/{time4alert}_nf.csv"
    # forecast_result = load_forecast_result(forecast_result_path)

    forecast_result = 1

    # Determine if an alert should be issued
    alert_info = determine_natural_resource_alert(forecast_result, time4alert)
    print(f'The natural resource alert result is {alert_info}.')
    print('------------------')
    # Store the hydrological alert result
    store_alert(alert_info, time4alert)
    return f'The natural resource alert result is {alert_info}.'


def store_alert(alert_info, time4alert):
    print('store the natural resource alert')
    print('------------------')
    alert_path = f"{natural_resource_alert_root}/{time4alert}_na.json"
    os.makedirs(os.path.dirname(alert_path), exist_ok=True)

    with open(alert_path, 'w') as json_file:
        json.dump(alert_info, json_file, indent=4)

# # Load the natural resource forecast results
# def load_forecast_result(forecast_result_path):
#     if forecast_result_path.endswith('.nc'):
#         with nc.Dataset(forecast_result_path, 'r') as nc_file:
#             wave_height = nc_file.variables['wave_height'][:]
#             storm_surge = nc_file.variables['storm_surge'][:]
#             geo_hazard_prob = nc_file.variables['geo_hazard_prob'][:]
#             forecast_result = {
#                 'wave_height': wave_height,
#                 'storm_surge': storm_surge,
#                 'geo_hazard_prob': geo_hazard_prob
#             }
#     elif forecast_result_path.endswith('.npy'):
#         forecast_result = np.load(forecast_result_path, allow_pickle=True).item()
#     elif forecast_result_path.endswith('.csv'):
#         data = pd.read_csv(forecast_result_path)
#         ocean_wave = extract_timeseries_by_type(data, 'Ocean Wave', 'wave_height_value')
#         storm_surge = extract_timeseries_by_type(data, 'Storm Surge', 'storm_surge_value')
#         geological_disaster = extract_timeseries_by_type(data, 'Geological Disaster', 'geological_disaster_value')
#         forecast_result = {'ocean_wave': ocean_wave, 'storm_surge': storm_surge, 'geological_disaster': geological_disaster}
#     else:
#         raise ValueError("Unsupported file format. Please provide a .nc or .npy file.")
#     return forecast_result
#
# def extract_timeseries_by_type(df, data_type, value_column, unique_id_column='name', time_steps=24):
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
#     filtered_data = df[df['disaster_type'] == data_type]
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

# Determine if a natural resource alert should be issued
def determine_natural_resource_alert(forecast_result, time4alert):
    print(f'determine the natural resource alert at time {time4alert}')
    print('------------------')
    # Alert threshold conditions
    # wave_height_thresholds = {
    #     'blue': 2.0,    # Wave height thresholds in meters
    #     'yellow': 4.0,
    #     'orange': 6.0,
    #     'red': 8.0
    # }
    # storm_surge_thresholds = {
    #     'blue': 0.5,    # Storm surge thresholds in meters
    #     'yellow': 1.0,
    #     'orange': 1.5,
    #     'red': 2.0
    # }
    # geo_hazard_prob_threshold = 60  # Geological hazard probability threshold
    #
    # # Calculate the maximum wave height over the future period
    # max_wave_height = np.max(forecast_result['ocean_wave'])
    # print(f'Maximum wave height is {max_wave_height} meters')
    # wave_alert_level = 5
    # wave_alert_content = ''
    #
    # # Wave alert determination
    # if max_wave_height >= wave_height_thresholds['red']:
    #     wave_alert_level = 1
    #     wave_alert_content = 'Wave Red Alert'
    # elif max_wave_height >= wave_height_thresholds['orange']:
    #     wave_alert_level = 2
    #     wave_alert_content = 'Wave Orange Alert'
    # elif max_wave_height >= wave_height_thresholds['yellow']:
    #     wave_alert_level = 3
    #     wave_alert_content = 'Wave Yellow Alert'
    # elif max_wave_height >= wave_height_thresholds['blue']:
    #     wave_alert_level = 4
    #     wave_alert_content = 'Wave Blue Alert'
    #
    # # Calculate the maximum storm surge intensity over the future period
    # max_storm_surge = np.max(forecast_result['storm_surge'])
    # print(f'Maximum storm surge is {max_storm_surge} meters')
    # storm_surge_alert_level = 5
    # storm_surge_alert_content = ''
    #
    # # Storm surge alert determination
    # if max_storm_surge >= storm_surge_thresholds['red']:
    #     storm_surge_alert_level = 1
    #     storm_surge_alert_content = 'Storm Surge Red Alert'
    # elif max_storm_surge >= storm_surge_thresholds['orange']:
    #     storm_surge_alert_level = 2
    #     storm_surge_alert_content = 'Storm Surge Orange Alert'
    # elif max_storm_surge >= storm_surge_thresholds['yellow']:
    #     storm_surge_alert_level = 3
    #     storm_surge_alert_content = 'Storm Surge Yellow Alert'
    # elif max_storm_surge >= storm_surge_thresholds['blue']:
    #     storm_surge_alert_level = 4
    #     storm_surge_alert_content = 'Storm Surge Blue Alert'
    #
    #
    # # Calculate the maximum geological hazard probability over the future period
    # max_geo_hazard_prob = np.max(forecast_result['geological_disaster'])
    # print(f'Maximum geological disaster probability is {max_geo_hazard_prob}')
    # geo_hazard_alert_level = 5
    # geo_hazard_alert_content = ''
    #
    # # Geological hazard alert determination
    # if max_geo_hazard_prob >= geo_hazard_prob_threshold:
    #     geo_hazard_alert_level = 3
    #     geo_hazard_alert_content = 'Geological Disaster Alert'
    #
    #
    # alert_content = wave_alert_content + ', ' + storm_surge_alert_content + ', ' + geo_hazard_alert_content
    #
    # alert_level = min(wave_alert_level, storm_surge_alert_level, geo_hazard_alert_level) % 5
    natural_resource_alert = {
        "natural_resource_alert_level": 1,
        "natural_resource_alert_content": "Wave Red Alert, Storm Surge Red Alert, Geological Disaster Alert"
    }
    return natural_resource_alert

# Tool invocation example
if __name__ == "__main__":
    # Initialize input parameters
    current_time = '2022091320'  # Example current time in YYYYMMDDHH format

    # Create an instance of NaturalResourceAlertTool
    natural_resource_alert_tool = NaturalResourceAlertTool()

    # Invoke the tool
    alert_info = natural_resource_alert_tool._run(time4alert=current_time)

    # Print the results
    # print("Natural Resource Alert Information:")
    # print(alert_info)
