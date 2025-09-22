import json
import os
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from config.root_base import *  # Ensure this is correctly configured in your project


# Define the input schema for the HydraulicRepairTool
class HydraulicRepairInput(BaseModel):
    time4repair: str = Field(
        description="The timestamp for hydraulic repair plan formulation, format in YYYYMMDDHH"
    )
    location4repair: str = Field(
        default="whole province",  # Default value for location is "whole province"
        description="The geographic location for the hydraulic repair plan. It could be a city, region, or specific coordinates."
    )


# Define the HydraulicRepairTool class
class HydraulicRepairTool(BaseTool):
    name: str = "hydraulic_repair_tool"
    description: str = "Useful to schedule hydraulic repair work on hydraulic engineering infrastructure."
    args_schema: Type[BaseModel] = HydraulicRepairInput

    def _run(self, time4repair: str, location4repair: str):
        # Logic to perform scheduling based on current project status and resources
        return mainHydraulicRepair(time4repair, location4repair)

    def _arun(self, time4repair: str, location4repair: str):
        raise NotImplementedError("repair_tool does not support async")


# Function to store the repair plan as a JSON file
def store_repair(repair_schedule: dict, time4repair: str):
    disaster_name = 'Lekima'  # You can adjust this to dynamically fetch disaster name
    repair_path = f'{hydraulic_repair_root}/{disaster_name}-{time4repair}_hydro_repair.json'
    os.makedirs(os.path.dirname(repair_path), exist_ok=True)
    with open(repair_path, 'w') as json_file:
        json.dump(repair_schedule, json_file, indent=4)


# Main function to create the hydraulic repair plan
def mainHydraulicRepair(time4repair: str, location4repair: str):
    print(f"Starting hydraulic repair scheduling for {location4repair} at {time4repair}")
    print('-------------------')

    # Example project status and resources
    project_status = {
        'dam': {'status': 'damaged', 'severity': 0.8},
        'canal': {'status': 'operational', 'severity': 0.2},
        'pump_station': {'status': 'damaged', 'severity': 0.5}
    }

    resource_status = {
        'workers': 200,
        'equipment': {'cranes': 2, 'bulldozers': 3},
        'materials': {'cement': 100, 'steel': 50}
    }

    # Sorting the projects based on severity (highest first)
    sorted_projects = sorted(project_status.items(), key=lambda x: x[1]['severity'], reverse=True)

    repair_plan = []
    for project, status in sorted_projects:
        if status['status'] == 'damaged':
            required_workers = int(status['severity'] * 20)  # Hypothetical calculation of worker requirements
            if resource_status['workers'] >= required_workers:
                repair_plan.append(f"Repair {project} with {required_workers} workers.")
                resource_status['workers'] -= required_workers
            else:
                repair_plan.append(f"Not enough workers to repair {project}. Assigning available resources.")
                return f"Not enough workers to repair {project}. Assigning available resources."

    repair_res = {
        'currentTime': time4repair,
        'repair_plan': repair_plan,
        'remaining_resources': resource_status
    }

    # Store the repair plan
    store_repair(repair_res, time4repair)

    return f"Hydraulic repair schedule for {time4repair} has been completed."


# Example usage:
if __name__ == "__main__":
    hydropower_repair_tool = HydraulicRepairTool()

    # Call the tool with parameters
    res = hydropower_repair_tool._run('2022091320', 'whole province')  # Example time and location
    print(res)
