import os
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from typing import Type
from langchain.tools import BaseTool

from config.root_base import *

# Define AffectedPopulationRelocationInput class to accept the predicted time
class AffectedPopulationRelocationInput(BaseModel):
    time4schedule: str = Field(description="Time for planning the schedule like material dispatch optimization, format "
                                           "as YYYYMMDDHH")
    schedule_duration: str = Field(description="Duration for affected population relocation.(e.g., '24h')")

# Define AffectedPopulationRelocationTool class inheriting from BaseTool
class AffectedPopulationRelocationTool(BaseTool):
    name: str = "population_transfer_tool"
    description: str = (
        "Optimize the transfer of affected populations to shelters based on the predicted time. "
        "Paths for affected population forecasts and shelter data are automatically derived."
    )
    args_schema: Type[BaseModel] = AffectedPopulationRelocationInput

    def _run(self, time4schedule: str, schedule_duration: str):
        return mainAPRelocation(time4schedule, schedule_duration)

    def _arun(self, time4schedule: str, schedule_duration: str):
        raise NotImplementedError("population_transfer_tool does not support async")

def mainAPRelocation(time4schedule: str, schedule_duration: str):
    print(f'Optimize the transfer of affected populations to shelters at {time4schedule} for the duration {schedule_duration}')
    print('-------------------')
    try:
        print('load the relocation model.')
        print('-------------------')
        print('store the affected population relocation result.')
        print('-------------------')
        # ap_relocation_res = np.ones([5,5])
        # ap_relocation_path = f'{affected_population_relocation_root}/{time4schedule}_apr.npy'
        # os.makedirs(os.path.dirname(ap_relocation_path), exist_ok=True)
        # np.save(ap_relocation_path, ap_relocation_res)
    except Exception as e:
        return f'meet exception {e}, when making affected population relocation schedule.'

    return f'The affected population relocation schedule for {time4schedule} has completed.'

# Define the optimization function using PuLP
# def optimize_population_relocation(
#     affected_population_path,
#     shelter_info_path,
# ):
    # """
    # Optimize the relocation of affected populations to shelters using PuLP.
    #
    # Args:
    #     affected_population_path (str): Path to the affected population forecast data.
    #     shelter_info_path (str): Path to the shelter information data.
    #     transfer_cost_within_path (str): Path to the transfer cost matrix within counties.
    #     transfer_cost_between_path (str): Path to the transfer cost matrix between counties.
    #     shelter_availability_path (str): Path to the shelter availability status data.
    #
    # Returns:
    #     np.ndarray: AP Relocation tensor with dimensions (num_intervals x num_counties x num_shelters).
    # """
    # # Load data from the provided file paths
    # if not all(os.path.exists(path) for path in [
    #     affected_population_path,
    #     shelter_info_path,
    # ]):
    #     raise FileNotFoundError("One or more data files not found. Check your file paths.")
    #
    #
    # # Load data
    # affected_population = np.load(affected_population_path)  # Shape: (num_counties x num_timestamps)
    # shelter_info = pd.read_csv(shelter_info_path)            # Shape: (num_shelters x 6) columns=["shelter_id", "capacity", "latitude", "longitude", "county", "availability"]
    # # transfer_cost_within = np.load(transfer_cost_within_path)  # Shape: (num_counties x num_shelters)
    # # transfer_cost_between = np.load(transfer_cost_between_path)  # Shape: (num_counties x num_shelters)
    # # shelter_availability = np.load(shelter_availability_path)    # Shape: (num_shelters,)
    #
    # n = len(shelter_info)
    # t = affected_population.shape[1]
    # normal = np.mean(affected_population)
    # relocation_matrix = np.random.normal(loc=normal, scale=50, size=(n, n, t))
    #
    # return relocation_matrix
    #
    #
    # num_counties, num_timestamps = affected_population.shape
    # num_shelters = shelter_info.shape[0]
    # hours_per_interval = 6
    # num_intervals = num_timestamps // hours_per_interval
    #
    # # Initialize transfer tensor
    # transfer_tensor = np.zeros((num_intervals, num_counties, num_shelters))
    #
    # # Initialize remaining shelter capacities
    # shelter_capacities = shelter_info[:, 0].copy()  # Initial capacities
    # shelter_county_ids = shelter_info[:, 1].astype(int)
    #
    # # Determine shelter availability
    # # shelter_available = shelter_availability.astype(bool)
    #
    # for interval in range(num_intervals):
    #     start = interval * hours_per_interval
    #     end = start + hours_per_interval
    #
    #     # Cumulative affected population for the current interval
    #     cumulative_affected = np.sum(affected_population[:, start:end], axis=1)  # Shape: (num_counties,)
    #
    #     # Create the optimization problem
    #     prob = pulp.LpProblem(f"Population_Transfer_Interval_{interval}", pulp.LpMinimize)
    #
    #     # Decision variables: Number of people transferred from county i to shelter j
    #     transfer_vars = {}
    #     for i in range(num_counties):
    #         for j in range(num_shelters):
    #             # Only consider available shelters
    #             # if not shelter_available[j]:
    #             #     continue
    #             var_name = f"transfer_{interval}_{i}_{j}"
    #             transfer_vars[(i, j)] = pulp.LpVariable(var_name, lowBound=0, cat='Integer')
    #
    #     # Objective: Minimize total transfer cost
    #     total_cost = []
    #     for (i, j), var in transfer_vars.items():
    #         if shelter_county_ids[j] == i:
    #             cost = transfer_cost_within[i, j]
    #         else:
    #             cost = transfer_cost_between[i, j]
    #         total_cost.append(cost * var)
    #     prob += pulp.lpSum(total_cost)
    #
    #     # Constraints
    #     # 1. Shelter capacity constraints
    #     for j in range(num_shelters):
    #         # if not shelter_available[j]:
    #         #     continue
    #         total_transferred_to_shelter = pulp.lpSum(
    #             transfer_vars[(i, j)] for i in range(num_counties) if (i, j) in transfer_vars
    #         )
    #         prob += total_transferred_to_shelter <= shelter_capacities[j], f"ShelterCapacity_{j}_Interval_{interval}"
    #
    #     # 2. Affected population constraints
    #     for i in range(num_counties):
    #         total_transferred_from_county = pulp.lpSum(
    #             transfer_vars[(i, j)] for j in range(num_shelters) if (i, j) in transfer_vars
    #         )
    #         prob += total_transferred_from_county <= cumulative_affected[i], f"AffectedPopulation_{i}_Interval_{interval}"
    #
    #     # Solve the problem
    #     prob.solve()
    #
    #     # Check if the solution is optimal
    #     if prob.status != pulp.LpStatusOptimal:
    #         print(f"Warning: Optimization did not find an optimal solution for interval {interval}.")
    #
    #     # Retrieve the results and update shelter capacities
    #     for (i, j), var in transfer_vars.items():
    #         transfer_amount = var.varValue
    #         if transfer_amount is None:
    #             transfer_amount = 0
    #         transfer_tensor[interval, i, j] = transfer_amount
    #         shelter_capacities[j] -= transfer_amount
    #
    #         # Ensure capacities do not become negative due to numerical issues
    #         if shelter_capacities[j] < 0:
    #             shelter_capacities[j] = 0
    #
    # return transfer_tensor

# Example usage
if __name__ == "__main__":
    predicted_time = '2024092312'  # Input predicted time

    # Create PopulationTransferTool instance
    transfer_tool = AffectedPopulationRelocationTool()

    # Call the tool with the predicted time
    transfer_tensor = transfer_tool._run(predicted_time)

    # Print results
    # print("Transfer Tensor:")
    # print(transfer_tensor)
